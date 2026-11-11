# SQLite to Neon PostgreSQL migration

## Completed

- The SQLite-to-Neon PostgreSQL data migration completed successfully.
- The original SQLite database and its backup were preserved.
- Neon migrations `0001` through `0008` were applied successfully.
- Migration `0007` increased `userreg.ph_no` from 10 to 15 characters.
- Migration `0008` increased `feedback.phone` from 10 to 15 characters.
- All four destination record counts were verified:

  | Model | Records |
  | --- | ---: |
  | `userreg` | 15 |
  | `vehicle_entry` | 14 |
  | `newbooking` | 30 |
  | `feedback` | 6 |
  | **Total** | **65** |

- The application uses PostgreSQL when `DATABASE_URL` is configured and falls
  back to SQLite when it is absent.
- The Render deployment configuration remains unchanged.

## Remaining deployment tasks

- Confirm Vercel has the required environment variables configured for the
  intended deployment environments. Do not store credentials or secrets in
  this document or in source control.
- Verify the deployed Vercel application connects to Neon, renders the
  homepage, and can read application records.
- Verify static assets load correctly in the deployed application.
