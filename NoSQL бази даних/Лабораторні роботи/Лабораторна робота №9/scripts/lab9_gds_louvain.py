import json
from pathlib import Path

from graphdatascience import GraphDataScience


URI = "bolt://127.0.0.1:7687"
GRAPH_NAME = "lab9-variant5-communities"
VARIANT = 5
MARKER = "nosql-lab9-variant5"
ROOT = Path(__file__).resolve().parents[1]
RESULT_PATH = ROOT / "results" / "lab9_results.json"


def records(frame):
    return json.loads(frame.to_json(orient="records", force_ascii=False))


def main():
    gds = GraphDataScience(URI, auth=None)

    version = str(gds.run_cypher("RETURN gds.version() AS version").iloc[0]["version"])
    previous = gds.run_cypher(
        """
        MATCH (lab:LaboratoryWork)
        RETURN count(lab) AS laboratoryWorks,
               count(CASE WHEN lab.variant = $variant THEN 1 END) AS variantFiveWorks
        """,
        params={"variant": VARIANT},
    ).iloc[0].to_dict()

    if gds.run_cypher(
        "CALL gds.graph.exists($name) YIELD exists RETURN exists",
        params={"name": GRAPH_NAME},
    ).iloc[0]["exists"]:
        gds.run_cypher(
            "CALL gds.graph.drop($name, false) YIELD graphName RETURN graphName",
            params={"name": GRAPH_NAME},
        )

    gds.run_cypher(
        "MATCH (member:AnalyticsMember {marker: $marker}) DETACH DELETE member",
        params={"marker": MARKER},
    )

    members = []
    for team, lab_number in (("Alpha", 7), ("Beta", 8), ("Gamma", 9)):
        for number in range(1, 5):
            members.append(
                {
                    "memberId": f"{team.lower()}-{number}",
                    "name": f"{team} {number}",
                    "team": team,
                    "labNumber": lab_number,
                }
            )

    gds.run_cypher(
        """
        UNWIND $members AS row
        CREATE (member:AnalyticsMember {
          memberId: row.memberId,
          name: row.name,
          expectedTeam: row.team,
          variant: $variant,
          marker: $marker
        })
        WITH member, row
        OPTIONAL MATCH (lab:LaboratoryWork {number: row.labNumber})
        FOREACH (_ IN CASE WHEN lab IS NULL THEN [] ELSE [1] END |
          CREATE (member)-[:ANALYZES]->(lab)
        )
        """,
        params={"members": members, "variant": VARIANT, "marker": MARKER},
    )

    gds.run_cypher(
        """
        MATCH (left:AnalyticsMember {marker: $marker}),
              (right:AnalyticsMember {marker: $marker})
        WHERE left.expectedTeam = right.expectedTeam
          AND left.memberId < right.memberId
        CREATE (left)-[:COLLABORATES {weight: 1.0}]->(right)
        """,
        params={"marker": MARKER},
    )
    gds.run_cypher(
        """
        MATCH (alpha:AnalyticsMember {memberId: 'alpha-4', marker: $marker}),
              (beta1:AnalyticsMember {memberId: 'beta-1', marker: $marker}),
              (beta4:AnalyticsMember {memberId: 'beta-4', marker: $marker}),
              (gamma:AnalyticsMember {memberId: 'gamma-1', marker: $marker})
        CREATE (alpha)-[:COLLABORATES {weight: 0.15}]->(beta1),
               (beta4)-[:COLLABORATES {weight: 0.15}]->(gamma)
        """,
        params={"marker": MARKER},
    )

    dataset = gds.run_cypher(
        """
        MATCH (member:AnalyticsMember {marker: $marker})
        OPTIONAL MATCH (member)-[relationship:COLLABORATES]-()
        RETURN count(DISTINCT member) AS nodes,
               count(DISTINCT relationship) AS relationships
        """,
        params={"marker": MARKER},
    ).iloc[0].to_dict()

    projection = gds.run_cypher(
        """
        CALL gds.graph.project(
          $name,
          'AnalyticsMember',
          {COLLABORATES: {orientation: 'UNDIRECTED', properties: 'weight'}}
        )
        YIELD graphName, nodeCount, relationshipCount, projectMillis
        RETURN graphName, nodeCount, relationshipCount, projectMillis
        """,
        params={"name": GRAPH_NAME},
    ).iloc[0].to_dict()

    streamed = gds.run_cypher(
        """
        CALL gds.louvain.stream($name, {
          relationshipWeightProperty: 'weight',
          consecutiveIds: true
        })
        YIELD nodeId, communityId, intermediateCommunityIds
        RETURN gds.util.asNode(nodeId).memberId AS memberId,
               gds.util.asNode(nodeId).name AS name,
               gds.util.asNode(nodeId).expectedTeam AS expectedTeam,
               communityId,
               intermediateCommunityIds
        ORDER BY communityId, memberId
        """,
        params={"name": GRAPH_NAME},
    )

    stats = gds.run_cypher(
        """
        CALL gds.louvain.stats($name, {
          relationshipWeightProperty: 'weight',
          consecutiveIds: true
        })
        YIELD communityCount, modularity, modularities, ranLevels, computeMillis
        RETURN communityCount, modularity, modularities, ranLevels, computeMillis
        """,
        params={"name": GRAPH_NAME},
    ).iloc[0].to_dict()

    write = gds.run_cypher(
        """
        CALL gds.louvain.write($name, {
          relationshipWeightProperty: 'weight',
          writeProperty: 'communityId',
          consecutiveIds: true
        })
        YIELD communityCount, modularity, nodePropertiesWritten, writeMillis
        RETURN communityCount, modularity, nodePropertiesWritten, writeMillis
        """,
        params={"name": GRAPH_NAME},
    ).iloc[0].to_dict()

    persisted = gds.run_cypher(
        """
        MATCH (member:AnalyticsMember {marker: $marker})
        RETURN member.communityId AS communityId,
               count(*) AS members,
               collect(member.name) AS names,
               collect(DISTINCT member.expectedTeam) AS expectedTeams
        ORDER BY communityId
        """,
        params={"marker": MARKER},
    )

    gds.run_cypher(
        "CALL gds.graph.drop($name, false) YIELD graphName RETURN graphName",
        params={"name": GRAPH_NAME},
    )
    graph_exists_after = bool(
        gds.run_cypher(
            "CALL gds.graph.exists($name) YIELD exists RETURN exists",
            params={"name": GRAPH_NAME},
        ).iloc[0]["exists"]
    )

    stream_rows = records(streamed)
    persisted_rows = records(persisted)
    checks = {
        "gdsConnected": bool(version),
        "previousGraphLoaded": int(previous["laboratoryWorks"]) >= 7,
        "variantFiveLoaded": int(previous["variantFiveWorks"]) >= 7,
        "datasetCreated": int(dataset["nodes"]) == 12,
        "relationshipsCreated": int(dataset["relationships"]) == 20,
        "projectionCreated": int(projection["nodeCount"]) == 12,
        "threeCommunitiesFound": int(stats["communityCount"]) == 3,
        "allNodesStreamed": len(stream_rows) == 12,
        "propertiesWritten": int(write["nodePropertiesWritten"]) == 12,
        "communitiesPersisted": len(persisted_rows) == 3,
        "teamsNotSplit": all(len(row["expectedTeams"]) == 1 for row in persisted_rows),
        "projectionDropped": not graph_exists_after,
    }
    if not all(checks.values()):
        raise RuntimeError(f"Lab 9 validation failed: {checks}")

    result = {
        "lab": 9,
        "variant": VARIANT,
        "student": "Левченко Д. В.",
        "reviewer": "Андреєв П. І.",
        "neo4j": {"uri": URI, "gdsVersion": version},
        "previousGraph": previous,
        "dataset": dataset,
        "projection": projection,
        "louvain": {
            "stats": stats,
            "stream": stream_rows,
            "write": write,
            "persistedCommunities": persisted_rows,
        },
        "projectionExistsAfterDrop": graph_exists_after,
        "checks": checks,
    }
    RESULT_PATH.parent.mkdir(parents=True, exist_ok=True)
    RESULT_PATH.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    gds.close()


if __name__ == "__main__":
    main()
