// Code JavaScript Run Once for All Items.
return $input.all().map((item, i) => {
  const r = item.json;
  const valid = ["agendar", "informacion", "revision"].includes(r.category)
    && typeof r.confidence === "number" && Number.isFinite(r.confidence)
    && r.confidence >= 0 && r.confidence <= 1
    && typeof r.needs_human === "boolean";
  return {json: {...r, classification_valid: valid}, pairedItem: {item: i}};
});
