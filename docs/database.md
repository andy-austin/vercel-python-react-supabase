# Database Documentation

## Supabase Configuration

### Setup
The database package (`packages/db`) provides Supabase client configuration and TypeScript type definitions.

### Environment Variables
```env
NEXT_PUBLIC_SUPABASE_URL=https://your-project.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-anon-key
```

### Client Usage
```typescript
import { supabase } from 'db'

// Query data
const { data, error } = await supabase
  .from('users')
  .select('*')

// Insert data
const { data, error } = await supabase
  .from('users')
  .insert({ email: 'user@example.com', name: 'John Doe' })
```

## Type Generation

### Generate Types
```bash
cd packages/db
pnpm gen-types
```

This command:
1. Connects to your Supabase database
2. Generates TypeScript types from your schema
3. Saves types to `supabase/types.ts`

### Using Generated Types
```typescript
import type { Database } from 'db'

type User = Database['public']['Tables']['users']['Row']
type UserInsert = Database['public']['Tables']['users']['Insert']
type UserUpdate = Database['public']['Tables']['users']['Update']
```

## Schema Management

### Local Development
For local development with Supabase CLI:

```bash
# Start local Supabase
supabase start

# Apply migrations
supabase db push

# Generate types for local instance
supabase gen types typescript --local > supabase/types.ts
```

### Migrations
Create and apply database migrations:

```bash
# Create migration
supabase migration new add_users_table

# Apply to remote
supabase db push
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