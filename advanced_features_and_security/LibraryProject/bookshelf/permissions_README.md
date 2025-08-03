# Permission & Groups Setup

## Custom Permissions (on `Book` model)
- `can_view`   — Can view the list or details of a book.
- `can_create` — Can create a new book.
- `can_edit`   — Can edit an existing book.
- `can_delete` — Can delete a book.

## Groups:
- **Viewers**: `can_view`
- **Editors**: `can_view`, `can_create`, `can_edit`
- **Admins**: All permissions

## Usage in Views:
Use Django's `@permission_required('bookshelf.can_edit')` decorator to enforce role-based access.

## Setup Script:
Run the following command to auto-create groups and assign permissions:

```bash
python manage.py setup_permissions
