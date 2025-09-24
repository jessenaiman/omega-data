# Data Model: Persistent Scene Flow API

## Entities

### Party
| Field | Type | Description |
|-------|------|-------------|
| id | UUID | Internal record ID (primary key) |
| session_id | String | Public session identifier (e.g., "shard-472-demo") |
| name | String | Party name |
| heroes | JSON | List of hero objects (name, class, hp) |
| symbol_choice | String | Player's chosen symbol (nullable) |
| scene_index | Integer | Current scene (1-11) |
| choices | JSON | Map of scene decisions |
| created_at | DateTime | Record creation time |
| updated_at | DateTime | Last save time |

## Relationships
- No relationships needed - single table design

## Validation Rules
- session_id must be unique
- scene_index must be between 1 and 11
- heroes list must contain valid hero objects
- choices must be a valid JSON object

## State Transitions
- New party: scene_index = 1, empty heroes, no choices
- Progress through scenes: scene_index increments based on player choices
- Symbol choice is set when player makes selection
- All state preserved on save/load operations