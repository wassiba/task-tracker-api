# Personal AI-Usage Rules

## 1. Purpose and Scope

This policy governs how I use AI tools in educational, personal, and professional work. It covers all AI-assisted work and decisions.

I will follow the strictest applicable organizational, contractual, legal, client, repository, project, production, and course requirements.

I will use AI as an assistant, not as a substitute for judgment, authorization, understanding, verification, or accountability. I remain responsible for what I submit, which actions I authorize, what evidence I accept, and whether generated work is suitable to retain or present as my own.

## 2. Information I Will Not Share with an Unapproved AI Tool

I will not submit personal information about anyone to a public, consumer, external, or otherwise unapproved AI tool. This includes identifying, financial, medical, biometric, precise-location, private-communication, employment, educational, and authentication-related information.

I will not paste operational secrets into ordinary AI prompts. This prohibition includes passwords, credentials, tokens, API keys, private keys, session cookies, authentication codes, recovery codes, production secrets, and `.env` contents. I will use synthetic placeholders or an approved purpose-built secret-handling mechanism instead.

Sensitive information may be processed only in an access-controlled AI environment explicitly authorized for its classification, ownership, intended purpose, jurisdiction, access controls, retention policy, and deletion requirements. Before using such an environment, I must confirm my authority, minimize the information, and comply with applicable legal, contractual, organizational, client, course, and governance requirements. I must also confirm acceptable access, reuse, retention, and deletion controls.

Authorization of an environment is a prerequisite, not automatic permission to submit every sensitive item.

## 3. Conditions for Sharing Private Project Information

I may share private but non-sensitive material when it is necessary for a clearly defined and authorized task. Examples include authorized source code, tests, documentation, technical decisions, sanitized operational evidence, course material, and secret-free configuration or metadata.

Before sharing, I will confirm that:

- I created and still control the material, or the authorized owner permits the intended AI use.
- Written permission, a licence, course rule, organizational policy, or documented governance decision permits the use when I rely on it.
- The selected AI environment is approved for the material.
- The tool's access, retention, reuse, and deletion terms are acceptable.
- The content is necessary and proportionate to the task.

Possessing a copy, purchasing access, holding repository permissions, or finding material publicly visible does not itself establish permission to submit it. Educational use and convenience are not substitutes for authorization. I will share course or third-party material only when its permitted use has been established. If ownership, permission, sensitivity, or tool authorization is uncertain, I will pause and seek confirmation from the appropriate authority.

## 4. Context Minimization and Sanitization

I will provide minimum necessary context, preferring excerpts or named files, then bounded directories, over whole repositories or workspaces.

Before sharing content, I will inspect it for secrets and unrelated personal, account, machine, or project information. I will sanitize or omit:

- Names, usernames, account details, email addresses, and identifiers.
- Absolute local paths and unrelated directory names.
- Browser chrome, open tabs, notifications, and account indicators.
- Tokens, cookies, authentication headers, connection strings, and secret values.
- Machine names, process listings, environment output, and unrelated configuration.
- Unnecessary repository, CI, service, and infrastructure metadata.
- Third-party content not authorized for the task.

I will prefer concise extracts and summarized results over unrestricted logs, screenshots, browser captures, or environment dumps. I will review screenshots and logs before submission rather than assume they are safe. Sanitization does not create permission to share prohibited material.

## 5. Repository Access and Approval Boundaries

By default, I will give repository-aware AI tools read-only access to selected excerpts or explicitly named files required for a defined task. If individual files are insufficient, I may grant access to the smallest relevant directory.

Before repository-aware work, I will define the objective, readable scope, editable-file allowlist, prohibited files and actions, verification requirements, and stopping conditions. Broader repository or workspace access requires evidence that narrower access is insufficient. Before expanding access, I will exclude secrets, credentials, `.env` files, ignored files, personal information, local environments, caches, generated artifacts, and unrelated material. If technical controls cannot enforce the boundary, I will use an isolated working copy or approved environment containing only permitted material.

A precisely scoped request may itself constitute the required fresh approval when it explicitly authorizes the consequential action and identifies its scope and consequences. No redundant second confirmation is required for the same expressly authorized operation. Fresh approval is required when the operation was not explicitly authorized, when its scope or consequences change, or when new uncertainty arises.

This approval rule applies without weakening the boundaries for staging, committing, pushing, tagging, branch changes, merging, rebasing, amending, resetting, history rewriting, force-pushing, dependency changes, CI, Docker, deployment, external services, sensitive information, destructive actions, and other consequential operations. The request must expressly authorize the applicable operation; general permission to investigate or edit does not imply it.

Consequential operations also include builds, containers, servers, scanners, network transmission, cloud, account, billing, shared-resource, and externally visible actions. I will pause if a tool seeks broader access or authority.

## 6. Verification and Acceptance

I will treat AI-generated changes and material claims as unverified until supported by appropriate evidence. Before acceptance, I will review the complete affected diff, confirm that only approved files changed, and check for unsupported claims, placeholders, secrets, and unrelated edits. A passing test does not replace diff review, and I will not claim a result I did not observe.

I will run formatting, syntax, link, structural, or other checks appropriate to the artifact and record what was and was not verified.

For application-code changes, I will run focused tests, exercise important negative and boundary cases, and use manual or runtime verification when automated tests do not cover the user-facing result. I will run the full regression suite before an approved commit or significant milestone.

For documentation-only changes, I will verify factual claims against repository or execution evidence and check paths, commands, links, Markdown, encoding, and whitespace. Full regression testing may be omitted only when the reason and approved verification boundary are explicitly documented.

For CI, Docker, dependencies, security, deployment, or data-handling changes, I will inspect the exact configuration diff and consult current authoritative evidence. When the consequential operation has been expressly approved under Section 5, I will perform the relevant build, runtime, scanner, or environment verification.

Dated historical evidence may remain valid as a record of what was observed. I will not treat it as proof of current mutable versions, advisories, dependency status, image contents, external documentation, or service state. I will renew the evidence before a current consequential claim or decision.

## 7. Higher-Risk Work

I will require stronger verification and independent human review for work involving:

- Authentication, authorization, permissions, access control, secrets, encryption, cryptography, identity, or vulnerabilities.
- Personal, customer, financial, medical, or regulated data.
- Dependencies, software supply chains, CI/CD, Docker, infrastructure, deployment, or external integrations.
- Database schemas, migrations, backups, recovery, or destructive data operations.
- Git history rewriting, force-pushing, releases, or production incidents.
- Material effects on billing, shared resources, external users, legal rights, licensing, privacy, or third-party authorization.

Reviewer qualifications must match the risk. Security-sensitive work requires relevant security expertise; infrastructure work requires an operations or platform specialist; migration and recovery work requires database or data-integrity expertise; and privacy, licensing, disclosure, or authorization questions require an appropriately authorized legal, privacy, licensing, or governance representative. Business-rule and user-impact decisions require the project owner or a knowledgeable domain expert.

For course work, an instructor or suitably knowledgeable peer may review according to the consequences and course rules. Professional work may require an authorized specialist or accountable owner. Independent review means substantive examination by someone other than the AI system and sole producer.

Stronger review does not automatically require changing a known limitation. An intentional project or course limitation remains unchanged unless remediation is separately justified, expressly authorized, and verified.

## 8. Evidence and Recordkeeping

I will retain an AI-assistance record when AI materially influences a retained deliverable or significant technical or governance decision. I will always document involvement affecting security, privacy, dependencies, CI, Docker, Git, deployment, data handling, course milestones, consequential corrections or rejections, later-verification claims, or authorized third-party material.

An interaction is material when it changes a retained deliverable, affects risk or user outcomes, supports an approval or assessment, or matters when reproducing, auditing, or explaining the work. Trivial autocomplete, minor wording suggestions, brainstorming, and discarded output that do not affect retained work need not be recorded.

Where relevant, the record will identify:

- Date, tool, task, and purpose.
- Categories of information shared.
- The prompt or a faithful non-sensitive summary.
- Material output and whether it was accepted, adapted, rejected, or deferred.
- Human reasoning, approvals, affected files, and relevant diff.
- Verification evidence, sources, confidence, limitations, unknowns, and follow-up work.

Non-sensitive project records may be kept in repository documentation. Cross-project course records may be kept in an approved access-controlled knowledge base. Private or sensitive governance evidence must remain in an approved restricted system. Ordinary repository records must not contain secrets, sensitive values, unnecessary third-party material, or private prompt contents.

I will normally retain significant records for the project's lifetime plus twelve months, or longer when required by applicable course, organizational, contractual, legal, audit, or governance rules. Records supporting continuing architecture, releases, security decisions, or consequential approvals may remain until the related system or decision is retired and no audit need remains. Private or authorized third-party material will be deleted when its approved purpose and applicable retention obligations end.

## 9. Ownership and Explainability

Before claiming AI-generated work as my own, I must understand it well enough to take informed responsibility for its accuracy, behavior, and consequences. For every retained artifact, I must be able to explain:

- Its purpose and intended outcome.
- Its material behavior or factual claims.
- Its inputs, outputs, dependencies, and side effects.
- Important assumptions, limitations, and failure modes.
- How it fits the surrounding project.
- What was verified and what remains unverified.

For documentation, I must support every material factual claim with evidence rather than rely on polished wording.

Required depth increases with risk. Foundational or higher-risk work involving security controls, identity, cryptography, data handling, migrations, CI/CD, Docker, infrastructure, deployment, or destructive operations requires line-by-line or instruction-by-instruction understanding, appropriate verification, and suitably qualified independent review. Lower-risk work may not require that depth, but I must understand all materially relevant behavior and claims.

I may conduct isolated temporary experiments before reaching full understanding if they are not merged, submitted, deployed, or represented as completed or owned work. If understanding remains incomplete, I will investigate, test, seek qualified review, narrow the retained work to what I can defend, or reject it. I will not conceal uncertainty or claim verification, comprehension, responsibility, or ownership that I cannot substantiate.

## 10. Pause, Rejection, and Escalation

I will pause when scope, outcome, access, or authority is unclear; new files, permissions, sensitive information, or consequential actions become necessary; evidence conflicts; or an important claim cannot be verified. I will also pause over uncertain ownership, licensing, privacy, authorization, tool approval, or current authoritative evidence. Work may continue after resolution, express approval, or safe narrowing.

I will reject a task when it requires:

- Disclosure of secrets or sensitive information to an unapproved system.
- Violation of applicable law, contract, policy, course rules, repository instructions, or an explicit safety boundary.
- Unauthorized access, deceptive evidence, concealed changes, or misrepresentation of work not performed or verified.
- A destructive or dangerous action that cannot be narrowed, controlled, or made reasonably recoverable.
- Authority the requester does not possess and cannot obtain.

I will escalate to the authority whose expertise and accountability match the issue: the instructor for course or assessment ambiguity; the project or repository owner for scope and ownership; a security reviewer for vulnerabilities, credentials, incidents, or access control; an authorized legal, privacy, licensing, or governance representative for rights and data questions; the operations or platform owner for infrastructure and deployment; and the database or data owner for migration, deletion, recovery, or integrity risks.

Escalation does not itself authorize an action. I will proceed only after a clear decision expressly authorizes the action and identifies its scope and consequences. If circumstances later change, I will pause for renewed approval.

## 11. Policy Review and Updates

I will review this policy:

- At the beginning of a materially different project or AI environment.
- After a relevant security, privacy, authorization, verification, or governance incident.
- When applicable tool terms, organizational rules, course rules, laws, contracts, or data classifications materially change.
- At least annually while the policy remains actively used.

Each review will consider whether the policy still reflects the applicable tools, information types, risks, approval paths, retention duties, and verification practices. I will record material policy changes with their rationale and effective date.
