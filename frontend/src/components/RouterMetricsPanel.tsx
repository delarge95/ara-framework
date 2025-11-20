import React from "react";

const RouterMetricsPanel: React.FC = () => {
  // TODO: Integrar lógica de métricas del router y fallback
  return (
    <section className="router-metrics-panel">
      <h2>Métricas de Orquestador</h2>
      <div>
        <p>Visualiza métricas del router, fallback y lógica de pool.</p>
        {/* Aquí se mostrarán las métricas del router y fallback */}
      </div>
    </section>
  );
};

export default RouterMetricsPanel;
