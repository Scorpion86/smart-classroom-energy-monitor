# Report Outline - CPC357 Assignment 2

## Cover Page
- Course, assignment title, group members, date.

## 1. System Architecture (30%)
- High-level overview of the smart classroom energy monitor.
- Component details:
  - Device simulator
  - Pub/Sub ingestion
  - Cloud Function processing
  - BigQuery storage
  - Looker Studio visualization
- Architecture diagram (include in report).

## 2. Design Considerations (20%)
- Constraints (no physical sensors, PoC scope, cost, time).
- Design factors (latency, scalability, reliability).
- Trade-offs (simulated device vs real hardware; BigQuery vs Firestore; serverless vs VM).

## 3. Development Process (40%)
- Step-by-step setup (project, Pub/Sub, BigQuery, Function).
- Simulator execution and data publishing.
- Dashboard creation in Looker Studio.
- Screenshots/visuals:
  - Pub/Sub topic
  - BigQuery table
  - Looker Studio dashboard
- Link to code repository and environment setup.

## 4. Security Considerations (10%)
- IAM least privilege for publisher and function.
- Data protection: encryption at rest, access controls on BigQuery.
- Access control for dashboard (group members only).

## Appendix
- Sample message payload.
- BigQuery schema.
- Environment variables and config.
