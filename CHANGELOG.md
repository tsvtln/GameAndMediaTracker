[2026-04-10]
- Accounts app backend implementation
  - Created AppUser model extending AbstractUser with username-based authentication
  - Added Profile model with one-to-one relationship to AppUser (avatar, statistics counters)
  - Implemented custom user manager (AppUserManager) for user creation
  - Created user groups with permissions: Regular Users, Moderators, Verified Users
  - Built registration form with strong password validation (uppercase, lowercase, number, special char)
  - Implemented login/logout with proper error handling and message display
  - Added avatar upload with file validation (max 5MB, image formats only)
  - Implemented password change with same validation requirements
  - Auto-create profile and assign group on user registration using django signals
  - Configured media file serving for development and production (not fully tested in prod yet)
  - Updated profile navigation to show/hide buttons based on authentication and permissions (such as login, logout, register, admin etc.)
  - Added whitenoise and gunicorn and tested deployment on Azure. App is now live at https://tsvtln.com (but is at DEBUG=True for now until I finish with all the functionality and can focus on the production deployment and security hardening)

[2026-03-28]
- Added custom 404 error page
  - Created dedicated 404.html template with custom TV-style animation
  - Added 404 view and URL handler for testing
  - Styled Return to Home button with neon green theme
- Implemented responsive web design across entire project
  - Created responsive.css with mobile-first approach
  - Added breakpoints for mobile (480px), tablet (768px), desktop (1024px), and large screens (1920px)
  - Made all grids, navigation, forms, and modals responsive
  - Ensured retro aesthetic is preserved across all screen sizes
  - No Bootstrap - pure CSS media queries to maintain custom design

[2026-03-17]
- Screenshots
  - Implemented consistent screenshot grid and modal popout across ROM details, My Screenshots, 
      Latest and Top Rated pages; clicking a thumbnail opens a centered modal with full image, info and actions.
  - Added Add/Remove Favorites toggle in screenshot modals (behaves like Favorites page) 
      and synced behavior across all screenshot pages.
  - Standardized screenshot box sizing and object-fit behavior so thumbnails are uniform and contained.

- Forums
  - Added forum pages: index, board, thread, new-topic templates and basic views/urls in 'common' for display during HTML/CSS development.
  - Thread posts show a small left avatar with username/date inline and message on the next line. Replies use the same layout.
  - Adjusted a bit the Forum index layout.
  - Basic reply form, create topic form and thread view implemented (HTML-only).

- Accounts (login / register / profile)
  - Styled and completed login, profile and register pages.
  - Implemented avatar upload modal with preview and a Change Avatar flow (JS + CSS).
  - Implemented Change Password modal (fields + basic client-side behavior) to match avatar modal UX.

- Other fixes & improvements
  - Added/updated JS handlers for multiple pages (favorite-screenshots, rom-details) to improve UX and match behaviors.
  - Small layout and interaction fixes across ROMs, BIOS, SAVES, Favorites and Community pages (dropdowns, cursors, hover effects, buttons etc.).


[2026-03-14]
- Due to heavy amount of copy-pasting the same thing, there was a lot of duplicated CSS when scanned with 'jscpd'
  - Refactored the CSS to not have duplicates and to re-use the same styles for certain elements across the project
- Added Favorites main page and all relates Favorites pages
- Implemented modular HTML and CSS for all Favorites subpages:
  - Favorite ROMs
  - Favorite Screenshots
- Added Community main page
- Added Events subpage under Community

[2026-03-11]
- Added SAVES main page and all related SAVE pages
- Implemented modular HTML and CSS for all SAVE subpages:
  - all saves
  - details for a save file
  - upload
  - vault (my saves)
- Removed some future pages from the navigation dropdown to focus on core features and avoid clutter

[2026-03-10]
- Added delete button for a rom with confirmation popup modal
- Improved delete button styling for ROM and BIOS pages to match site style
- Fixed delete button modal placement and behavior for ROM details page
- Added BIOS main page and all related BIOS pages
- Implemented modular HTML and CSS for all BIOS subpages:
  - all files
  - compatibility
  - FAQ
  - legal
  - upload

[2026-03-09]
- Added ROMs main page and all related ROMs pages
- Implemented modular HTML and CSS for all ROMs subpages: 
  - top games
  - newly added
  - trending
  - most downloaded
  - genres
  - platforms
  - ROM details
  - upload ROM
- Added custom file upload buttons and live preview for box art
- Improved navigation and dropdown menus for ROMs
- Enhanced cursor and glow effects for interactive elements
- Refined layout and responsiveness for ROMs pages

[2026-03-05]
- Created the django apps: 'accounts', 'bios', 'reviews', 'roms', 'saves'
- Created very minimal and simple views and urls for each app, just to have a visualization during HTML and CSS development.
- Added About and Contacts info pages with CSS.
- Implemented About and Contacts views and URLs in the common app.
- Created a contact form (HTML only, ready for Django integration).
- Improved navigation bar by adding dropdown menu with styling and relevant places to go.
- Added Website News page displaying the changelog.

[2026-03-03]
- Created the initial 'common' Django app.
- Added base layout, navigation, and home page HTML templates.
- Built modular CSS for site layout, navigation, and home page styling.
