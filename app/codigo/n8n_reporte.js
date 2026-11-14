// Code node > Run Once for All Items. Cada item: escribieron y agendaron.
const filas = $input.all();
let total = 0;
let citas = 0;
for (const item of filas) {
  const a = Number(item.json.escribieron);
  const b = Number(item.json.agendaron);
  if (!Number.isFinite(a) || !Number.isFinite(b) || a < 0 || b < 0 || b > a) {
    throw new Error("Fila de reporte no válida");
  }
  total += a;
  citas += b;
}
return [{ json: { escribieron: total, agendaron: citas,
  conversion: total === 0 ? 0 : Number((100 * citas / total).toFixed(2)) } }];
