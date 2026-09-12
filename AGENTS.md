# Commit and push rule

For every project you change, finish each completed change by creating a Git
commit with a clear, descriptive message and pushing it to the project's
configured remote branch. This is standing user authorization; do not ask for
confirmation again for routine commits and pushes.

Run the checks appropriate to the change before committing. Commit your task's
changes, preserving unrelated user work. Verify the push succeeded and report
the commit and branch in the final response. If committing or pushing is blocked
by permissions, authentication, a missing remote, or a conflict, report the
specific blocker; do not claim the work has been pushed. Do not force-push or
discard unrelated work to satisfy this rule.
