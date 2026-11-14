// Extensión de IA real. Primero mapear category reason needs_human al primer nivel.
// Code JavaScript Run Once for All Items. No utiliza una confianza autodeclarada.
return $input.all().map((item, i) => {
  const r = item.json;
  const valid = ["agendar", "informacion", "revision"].includes(r.category)
    && typeof r.reason === "string" && r.reason.trim().length > 0
    && r.reason.length <= 240 && r.needs_human === true;
  return {json: {...r, classification_valid: valid}, pairedItem: {item: i}};
});
