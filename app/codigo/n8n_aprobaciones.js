// Code JavaScript Run Once for All Items. Nodo sugerido: PrepararAprobaciones.
return $input.all().map((item, i) => {
  const row = item.json;
  let reason = "";
  let payload;
  try { payload = JSON.parse(row.payload_json); }
  catch { reason = "json_invalid"; }
  if (row.estado !== "APROBADO") reason = "not_approved";
  if (!String(row.aprobado_por ?? "").trim()) reason = "reviewer_required";
  const rev = String(row.revision ?? "");
  if (!/^[1-9]\d*$/.test(rev) || rev !== String(row.aprobada_revision ?? "")) {
    reason = "revision_mismatch";
  }
  if (String(row.task_id ?? "").trim()) reason = "already_processed";
  if (!payload || payload.consent !== true || typeof payload.event_id !== "string") {
    reason = reason || "payload_invalid";
  }
  return {json: {...row, payload: payload ?? null, approval_valid: !reason, approval_error: reason,
    idempotency_key: payload ? "N10:" + payload.event_id + ":r" + rev : ""},
    pairedItem: {item: i}};
});
