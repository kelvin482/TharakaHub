# Styling Notes and Improvements

This document tracks current styling conflicts and safe improvements that can be
done without breaking existing pages.

## CSS Inventory (Current)

- Global base styles: `users/static/users/css/style.css`
- Auth-only styles: `users/static/users/style.css` (used by login/register)
- Dashboard styles: `users/static/users/css/dashboard.css`
- Jobs list/detail styles: `jobs/static/jobs/css/jobs.css`, `jobs/static/jobs/css/job_detail.css`
- Marketing styles: `marketing/static/marketing/css/marketing.css`

## Conflicts and Risks Observed

1. **Global tokens defined twice with different palettes**
   - `users/static/users/css/style.css` and `users/static/users/style.css` both
     define `:root` with different colors and typography.
   - This is safe today because the files are not loaded on the same page, but
     it becomes a conflict if a page starts importing both.

2. **Global `.btn` styling defined in multiple files**
   - `users/static/users/css/style.css` defines a base `.btn`.
   - `users/static/users/css/dashboard.css` re-defines `.btn` and variants.
   - On dashboard pages, the later file overrides the base style. This is fine
     if intentional, but can produce unexpected button shapes when mixing
     dashboard widgets with global components.

3. **Page-level CSS was affecting global `body`**
   - `jobs/static/jobs/css/job_detail.css` previously styled `body` directly.
   - Because job detail extends the global base layout, this could override
     navbar spacing and global background.

4. **Inline styles in templates**
   - `jobs/templates/jobs/list.html` contains a large `<style>` block with
     layout and card styles. This makes it harder to maintain consistency and
     can lead to duplicates with `jobs/static/jobs/css/jobs.css`.

5. **Unused CSS**
   - `users/static/users/css/jobs.css` is not referenced in templates.

## Improvements Implemented (Safe, No Behavior Change)

- Scoped job detail page body styling to a body class, so it no longer overrides
  global base styles.
- Moved job detail CSS into the head via the `extra_css` block for consistency.

Files changed:
- `users/templates/users/base.html`
- `jobs/templates/jobs/detail.html`
- `jobs/static/jobs/css/job_detail.css`

## Safe Improvements to Do Next

These are low risk and reduce conflicts without changing page layouts:

1. **Scope dashboard button rules**
   - Change global `.btn` rules in `users/static/users/css/dashboard.css` to
     `.dashboard-layout .btn` (or `.dashboard-scope .btn`) to prevent leaks into
     other pages if the stylesheet is reused.

2. **Normalize CSS variables**
   - Create a shared token set (colors, spacing, font scale) in one file, and
     let auth and base styles override only what is necessary.
   - This prevents mismatched `--primary`, `--accent`, and typography choices.

3. **Move inline styles into CSS**
   - Move the `<style>` block in `jobs/templates/jobs/list.html` into
     `jobs/static/jobs/css/jobs.css`.

4. **Reduce duplicate selectors**
   - There are multiple `.messages` and `.message` styles across files. Pick one
     base style and extend it in a scoped section to avoid accidental overrides.

5. **Remove or wire unused CSS**
   - Either delete `users/static/users/css/jobs.css` or include it intentionally.

## Design Improvement Ideas (Non-Conflicting)

- **Consistent spacing scale**: add a `--space-*` scale in the base stylesheet.
- **Shared typography scale**: define `--font-size-*` tokens instead of hard
  coded sizes.
- **Accessible button states**: add `:focus-visible` styles for keyboard users.
- **Card system**: create a `.card` base and apply per-page variants.

## Suggested Next Step

Pick one of these and I can implement it:

1. Scope dashboard button styles to avoid `.btn` conflicts.
2. Move the jobs list inline styles into `jobs/css/jobs.css`.
3. Create shared CSS variables for base + auth pages.
