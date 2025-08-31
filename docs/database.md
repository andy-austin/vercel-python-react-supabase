# Database Documentation

## Supabase Configuration

### Setup

The project uses dual database access patterns:
- **Frontend**: Direct Supabase client integration in `apps/web`
- **Backend**: SQLAlchemy with Alembic migrations in `apps/api`

### Environment Variables

```env
NEXT_PUBLIC_SUPABASE_URL=https://your-project.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-anon-key
```

### Frontend Client Usage (apps/web)

```typescript
import { createClient } from '@supabase/supabase-js'

const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
)

// Query data
const { data, error } = await supabase
  .from('users')
  .select('*')

// Insert data
const { data, error } = await supabase
  .from('users')
  .insert({ email: 'user@example.com', name: 'John Doe' })
```

### Backend ORM Usage (apps/api)

The API uses SQLAlchemy models defined in `apps/api/models/` with Alembic for migrations.

```python
from sqlalchemy.orm import Session
from .models import User
from .database import get_db

# Query data
def get_users(db: Session):
    return db.query(User).all()

# Insert data  
def create_user(db: Session, email: str, name: str):
    user = User(email=email, name=name)
    db.add(user)
    db.commit()
    return user
```

## Type Generation

### Generate Supabase Types

```bash
# Generate TypeScript types for frontend
supabase gen types typescript --project-id your-project-id > apps/web/types/supabase.ts
```

### Using Generated Types

```typescript
import type { Database } from '@/types/supabase'

type User = Database['public']['Tables']['users']['Row']
type UserInsert = Database['public']['Tables']['users']['Insert']
type UserUpdate = Database['public']['Tables']['users']['Update']
```

## Schema Management

### Backend Migrations (apps/api)

The Python API uses Alembic for database schema management:

```bash
# Create a new migration
pnpm migrate:create

# Apply migrations
pnpm migrate

# Manual migration commands (with venv activated)
cd apps/api
source ../../.venv/bin/activate
PYTHONPATH=../.. alembic revision --autogenerate -m "description"
PYTHONPATH=../.. alembic upgrade head
```

### Supabase CLI (Optional)

For direct Supabase management:

```bash
# Start local Supabase
supabase start

# Apply SQL migrations
supabase db push

# Generate types for local instance
supabase gen types typescript --local > apps/web/types/supabase.ts
```

## Row Level Security (RLS)

Example RLS policies for user data:

```sql
-- Enable RLS
ALTER TABLE users ENABLE ROW LEVEL SECURITY;

-- Users can only see their own data
CREATE POLICY "Users can view own data" 
ON users FOR SELECT 
USING (auth.uid() = id);

-- Users can only update their own data
CREATE POLICY "Users can update own data" 
ON users FOR UPDATE 
USING (auth.uid() = id);
```

## Best Practices

1. **Type Safety**: Always regenerate types after schema changes
2. **Security**: Use RLS policies for data protection
3. **Performance**: Use appropriate indexes and query optimization
4. **Migrations**: Version control all schema changes
5. **Environment**: Use environment-specific database URLs
