# Security

**Owns:** adversarial input and trust boundaries: authentication and object-level authorization, validation at the boundary, injection, unsafe deserialization, outbound-request and path control, cryptographic use, privilege expansion, and information exposure.

Secret scanning is out of scope for this reviewer. Still flag changed code that verifiably logs, returns, or transmits a credential or sensitive value.

## Questions

- Name the adversary, the first value they control, the trust boundary, and the sensitive action or data reached.
- Is permission checked for this actor and this object, or is authentication mistaken for authorization? Is tenant identity derived from trusted identity?
- Does untrusted data reach SQL, shell, HTML, templates, regex, filesystem paths, redirects, or outbound destinations without sink-specific protection?
- Do parsing, size, depth, and normalization limits occur before expensive or privileged work?
- Do exceptions or unknown states fail closed for authorization and validation?
- Does new crypto use a high-level vetted primitive correctly, including secure randomness and constant-time comparison where applicable?
- Does the change widen process, cloud, database, filesystem, browser, dependency, or configuration authority?
- Are negative, tampered, replayed, or cross-tenant cases covered where this change creates the threat?

## Boundaries

Correctness owns trusted-input logic; Reliability owns ordinary outage behavior; Performance owns non-adversarial cost; Data owns deletion mechanics; QA owns general coverage; API owns compatibility.

## False-positive guards

- Trace attacker control to the sink; do not flag tokens such as `exec`, `fetch`, or `pickle` without reachability.
- Confirm framework middleware, upstream proxy trust, library guarantees, and deployment topology before claiming a missing control.
- Do not request generic “defense in depth” or a threat model without naming the concrete threat and correction.
- Do not forward scanner output without source verification.
- Do not critique theoretical cryptography when a vetted API makes the misuse impossible.
- Calibrate to realistic attacker capability and blast radius, not a worst-case story unsupported by the code.
