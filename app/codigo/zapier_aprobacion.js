// Input Data: payload_json, estado, revision, aprobada_revision, aprobado_por.
if (inputData.estado !== "APROBADO") throw new Error("Estado no aprobado");
if (!String(inputData.aprobado_por ?? "").trim()) throw new Error("Falta revisor");
if (!/^[1-9]\d*$/.test(String(inputData.revision)) || String(inputData.revision) !== String(inputData.aprobada_revision)) {
  throw new Error("La aprobación corresponde a otra revisión");
}
const p = JSON.parse(inputData.payload_json);
if (p.consent !== true) throw new Error("Sin consentimiento booleano verdadero");
return { ...p, payload_json: JSON.stringify(p),
  idempotency_key: "Z10:" + p.event_id + ":r" + inputData.revision };
