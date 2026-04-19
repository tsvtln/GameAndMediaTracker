# CheckPoint - Permission Mixins

## Overview

All permission logic across the project is centralized in `CheckPoint/common/permissions.py`.  
Rather than repeating `if user.is_staff or user.groups...` checks in every view, these reusable mixins extend Django's 
`UserPassesTestMixin` and are mixed into any view that needs access control.

---

## Mixins

### `OwnerOrModeratorMixin`

**Purpose**: Allows access if the requesting user is the **owner** of the object, a **staff member**, or a **Moderator**.  
Used on delete views for ROMs, BIOS files, save files, and screenshots.

**Class attribute**:
- `owner_field = 'uploaded_by'` - the model field that holds the owner. 
Override in the view if the field name differs (e.g. `owner_field = 'author'`).

```python
class OwnerOrModeratorMixin(UserPassesTestMixin):
    owner_field = 'uploaded_by'

    def test_func(self):
        obj = self.get_object()
        user = self.request.user

        if user.is_staff or user.groups.filter(name='Moderators').exists():
            return True

        owner = getattr(obj, self.owner_field, None)
        return owner == user
```

**Example usage**:
```python
class ScreenshotDeleteView(LoginRequiredMixin, OwnerOrModeratorMixin, DeleteView):
    model = Screenshot
    owner_field = 'uploaded_by'
    success_url = reverse_lazy('my screenshots')
```

---

### `ModeratorOnlyMixin`

**Purpose**: Allows access **only** to staff members and Moderators.  
Used on views that should never be accessible to regular users (e.g. event creation, forum moderation actions).

```python
class ModeratorOnlyMixin(UserPassesTestMixin):
    def test_func(self):
        user = self.request.user
        return user.is_staff or user.groups.filter(name='Moderators').exists()
```

---

### `ModeratorOrVerifiedMixin`

**Purpose**: Allows access to staff, Moderators, **and Verified Users**.  
Used on BIOS upload views - Verified Users are trusted contributors allowed to upload BIOS files even though they are not full Moderators.

```python
class ModeratorOrVerifiedMixin(UserPassesTestMixin):
    def test_func(self):
        user = self.request.user
        if user.is_staff:
            return True
        return user.groups.filter(name__in=['Moderators', 'Verified Users']).exists()
```

---

### `CanDeleteContextMixin`

**Purpose**: A **context mixin** (not a gate mixin) that injects a `can_delete` boolean into the template context.  
Used on detail views to conditionally show/hide delete buttons in templates without duplicating the permission logic there.

**Class attribute**:
- `owner_field = 'uploaded_by'` - same convention as `OwnerOrModeratorMixin`.

```python
class CanDeleteContextMixin:
    owner_field = 'uploaded_by'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        obj = self.get_object()
        user = self.request.user

        can_delete = False
        if user.is_authenticated:
            if user.is_staff or user.groups.filter(name='Moderators').exists():
                can_delete = True
            else:
                owner = getattr(obj, self.owner_field, None)
                if owner == user:
                    can_delete = True

        context['can_delete'] = can_delete
        return context
```

**Template usage**:
```html
{% if can_delete %}
<form method="post" action="{% url 'delete-rom' rom.pk %}">
    {% csrf_token %}
    <button type="submit">Delete</button>
</form>
{% endif %}
```

---

## Permission Matrix

| Action                     | Regular User | Verified User | Moderator | Staff |
|----------------------------|:------------:|:-------------:|:---------:|:-----:|
| Upload ROM                 |      ✅       |       ✅       |     ✅     |   ✅   |
| Upload BIOS                |      ❌       |       ✅       |     ✅     |   ✅   |
| Upload Save                |      ✅       |       ✅       |     ✅     |   ✅   |
| Upload Screenshot          |      ✅       |       ✅       |     ✅     |   ✅   |
| Delete own content         |      ✅       |       ✅       |     ✅     |   ✅   |
| Delete any content         |      ❌       |       ❌       |     ✅     |   ✅   |
| Create / Delete Events     |      ❌       |       ❌       |     ✅     |   ✅   |
| Mark Event as Passed       |      ❌       |       ❌       |     ✅     |   ✅   |
| Delete Forum Threads/Posts |      ❌       |       ❌       |     ✅     |   ✅   |
| Access Django Admin        |      ❌       |       ❌       |     ❌     |   ✅   |

---

#### Next Page: [Signals](004_signals.md)

---

<div style="display: flex">
  <a href="../README.md">
    <svg width="20" height="20" fill="blue" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" fill="#000000" version="1.1" id="Capa_1" width="800px" height="800px" viewBox="0 0 495.398 495.398" xml:space="preserve">
    <g>
        <g>
            <g>
                <path d="M487.083,225.514l-75.08-75.08V63.704c0-15.682-12.708-28.391-28.413-28.391c-15.669,0-28.377,12.709-28.377,28.391     v29.941L299.31,37.74c-27.639-27.624-75.694-27.575-103.27,0.05L8.312,225.514c-11.082,11.104-11.082,29.071,0,40.158     c11.087,11.101,29.089,11.101,40.172,0l187.71-187.729c6.115-6.083,16.893-6.083,22.976-0.018l187.742,187.747     c5.567,5.551,12.825,8.312,20.081,8.312c7.271,0,14.541-2.764,20.091-8.312C498.17,254.586,498.17,236.619,487.083,225.514z"/>
                <path d="M257.561,131.836c-5.454-5.451-14.285-5.451-19.723,0L72.712,296.913c-2.607,2.606-4.085,6.164-4.085,9.877v120.401     c0,28.253,22.908,51.16,51.16,51.16h81.754v-126.61h92.299v126.61h81.755c28.251,0,51.159-22.907,51.159-51.159V306.79     c0-3.713-1.465-7.271-4.085-9.877L257.561,131.836z"/>
            </g>
        </g>
    </g>
    </svg>
  </a>
 <a style="margin-left: 10px" href="../README.md">Home</a>
</div>

---

