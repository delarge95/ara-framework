import React from "react";

const EmergencyStop: React.FC = () => {
  // TODO: Integrar lógica de parada de emergencia y control
  return (
    <section className="emergency-stop">
      <h2>Parada de Emergencia</h2>
      <div>
        <button>Detener Todo</button>
        <p>Control inmediato para detener la orquestación y modelos.</p>
        {/* Aquí se implementará la lógica de parada de emergencia */}
      </div>
    </section>
  );
};

export default EmergencyStop;
