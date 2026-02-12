# smog

Airtable employee lookup client for querying employee information and management chains.

## Setup

1. Install dependencies:
   ```bash
   poetry install
   ```

2. Configure application settings (optional):
   ```bash
   cp config.yaml.example config.yaml
   ```

   Edit `config.yaml` to customize:
   - `default_email_domain`: Domain to append when username provided without @ (e.g., "example.com")
   - Leave empty to require full email addresses

3. Configure secrets:
   ```bash
   cp secrets.yaml.example secrets.yaml
   ```

4. Edit `secrets.yaml` with your Airtable credentials:
   - `api_key`: Your Airtable API key
   - `base_id`: Your Airtable base ID
   - `table_name`: The name of your users table (e.g., "Users")

## Usage

Look up an employee by email:
```bash
smog user@example.com
```

Show detailed employee information:
```bash
smog user@example.com --details
```

## Development

Run tests:
```bash
poetry run pytest
```

Run type checking:
```bash
poetry run mypy src/
```
