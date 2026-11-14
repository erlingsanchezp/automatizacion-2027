// Code by Zapier > Run Javascript (sin SDK). Input Data: base y token.
const base = String(inputData.base).replace(/\/$/, "");
const registros = [];
let path = "/leads?offset=0&limit=2";
const visitadas = new Set();
for (let pagina = 0; pagina < 10 && path !== null; pagina++) {
  if (!path.startsWith("/leads?") || visitadas.has(path)) {
    throw new Error("Paginación no válida o repetida");
  }
  visitadas.add(path);
  const respuesta = await fetch(base + path, {
    headers: { Authorization: "Bearer " + inputData.token }
  });
  if (!respuesta.ok) throw new Error("HTTP " + respuesta.status);
  const cuerpo = await respuesta.json();
  if (!Array.isArray(cuerpo.data)) throw new Error("data debe ser una lista");
  registros.push(...cuerpo.data);
  path = cuerpo.next_path;
}
if (path !== null) throw new Error("Se alcanzó el máximo de páginas");
return {
  total: registros.length,
  event_ids: registros.map(r => r.event_id),
  lead_ids: registros.map(r => r.lead_id),
  sedes: registros.map(r => r.sede)
};
