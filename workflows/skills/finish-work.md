---
name: finish-work
description: Use this skill to record final acceptance, produce the guarded handoff, and finish the work item.
---

# Finish Work

This skill owns `final-acceptance` and `finished`; `/skill:maintain-work-context` owns their signed checkpoints. Keep workflow evidence and chronological completion in the work repository under the [artifact boundary](../references/artifact-boundary.md), and use the [human review packet](../references/human-review-packet.md) for the final handoff.

## Confirm Acceptance

Require a current `final-review` gate and the human's explicit acceptance of the exact reviewed branches and commits. Reconcile those with current HEADs and uncommitted changes. Leave excluded, disjoint changes untouched and report them separately.

An included later commit or uncommitted change to a reviewed file makes review and acceptance stale. Request the backward transition to `implementation`, rerun affected work and verification through `/skill:plan-execution`, regain `implementation`, repeat `/skill:review-work`, and obtain explicit acceptance of the corrected target.

Request `final-acceptance` only for the unchanged accepted target. Continue only after `/skill:maintain-work-context` reports a valid signed checkpoint and a clean work repository.

## Prepare the Final Handoff

Give the human only manual confirmation steps required by the approved plan. Don't add other checks, even as a final step. If an approved screenshot or artifact requires human access, provide its exact location and the steps for getting that artifact/screenshot, rather than claiming to have collected it. Don't build complicated workarounds to get it yourself; asking the human is usually faster.

When a draft pull request is explicitly configured:

- confirm the accepted branch, remote, base branch, and available authentication, and require that no force push is needed;
- reuse an existing open or draft pull request for the same head and base when one exists;
- otherwise push only the accepted branch and create one draft pull request; and
- if access, configuration, eligibility, or an external action's outcome is uncertain, do not retry or guess. Return a local handoff with the repository, branch, commit, completed checks, and the human's next action.

When draft pull request creation is not configured, return that local handoff without publishing. Never mark a pull request ready, merge, deploy, release, or change ticket status.

## Record Completion

Append the final repository branches and commits plus the draft pull request or local handoff to `agent-journal.md`; leave current decisions and the completed checklist in `PLAN.md` without adding completion history. Request `finished`, verify the signed work-context commit, and require the work repository to be clean.

Report target repositories with uncommitted changes separately. Leave the finished work repository in place without adding a remote. Never force push, and push only as part of the configured draft pull request flow.
