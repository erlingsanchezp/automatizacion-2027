// Code JavaScript Run Once for All Items
const registros = [
  {
    "schema_version": "1.0",
    "event_id": "evt-001",
    "lead_id": "L001",
    "name": " Ana Torres ",
    "email": " ANA@EXAMPLE.COM ",
    "phone": "0990000001",
    "sede": "villaflora",
    "consent": true,
    "status": "nuevo",
    "created_at": "2027-01-15T14:00:00Z",
    "message": "Quiero información sobre limpieza"
  },
  {
    "schema_version": "1.0",
    "event_id": "evt-002",
    "lead_id": "L002",
    "name": "Luis Pérez",
    "email": "luis@example.com",
    "phone": "0990000002",
    "sede": "gran_aki_solanda",
    "consent": true,
    "status": "agendado",
    "created_at": "2027-01-15T15:00:00Z",
    "message": "Quiero agendar una cita"
  },
  {
    "schema_version": "1.0",
    "event_id": "evt-003",
    "lead_id": "L003",
    "name": "Marta Luna",
    "email": "marta@example.com",
    "phone": "0990000003",
    "sede": "solanda_la_j",
    "consent": false,
    "status": "nuevo",
    "created_at": "2027-01-15T16:00:00Z",
    "message": "Solo estoy revisando información"
  },
  {
    "schema_version": "1.0",
    "event_id": "evt-004",
    "lead_id": "L004",
    "name": "José Ríos",
    "email": "correo-invalido",
    "phone": "0990000004",
    "sede": "san_bartolo",
    "consent": true,
    "status": "nuevo",
    "created_at": "2027-01-15T17:00:00Z",
    "message": "Quiero información"
  },
  {
    "schema_version": "1.0",
    "event_id": "evt-005",
    "lead_id": "L005",
    "name": "Rosa Vega",
    "email": "rosa@example.com",
    "phone": "0990000005",
    "sede": "desconocida",
    "consent": true,
    "status": "nuevo",
    "created_at": "2027-01-15T18:00:00Z",
    "message": "Quiero agendar"
  }
];
return registros.map(registro => ({ json: registro }));
