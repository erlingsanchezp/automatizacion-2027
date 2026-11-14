function normalize(data) {
  if (data === null || typeof data !== "object" || Array.isArray(data)) {
    return { valid: false, eligible: false, errors: ["object_required"], data: {} };
  }
  const out = { ...data };
  out.name = String(data.name ?? "").trim().replace(/\s+/g, " ");
  out.email = String(data.email ?? "").trim().toLowerCase();
  out.sede = String(data.sede ?? "").trim().toLowerCase();
  out.consent = data.consent === true;
  const errors = [];
  for (const field of ["event_id", "lead_id", "name"]) {
    if (typeof data[field] !== "string" || !data[field].trim()) {
      errors.push(field + "_required");
    }
  }
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(out.email)) errors.push("email_invalid");
  const sedes = ["villaflora", "gran_aki_solanda", "solanda_la_j", "san_bartolo"];
  if (!sedes.includes(out.sede)) errors.push("sede_invalid");
  if (typeof data.consent !== "boolean") errors.push("consent_boolean_required");
  return { valid: errors.length === 0, eligible: errors.length === 0 && out.consent,
    errors, data: out };
}

if (typeof module !== "undefined") module.exports = { normalize };
