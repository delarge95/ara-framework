import React, { useState } from "react";
import { HashRouter, Routes, Route, Navigate } from "react-router-dom";
import { Layout } from "./components/Layout";
import { Dashboard } from "./components/Dashboard/Dashboard";
import { Leaderboard } from "./components/Documentation/Leaderboard";
import { Architecture } from "./components/Documentation/Architecture";
import { Concepts } from "./components/Learning/Concepts";
import { Glossary } from "./components/Glossary/Glossary";
import { Configuration } from "./components/Config/Configuration";
import { AppMode } from "./types";

const App: React.FC = () => {
  const [mode, setMode] = useState<AppMode>("pro");

  return (
    <HashRouter>
      <Layout mode={mode} setMode={setMode}>
        <Routes>
          <Route path="/" element={<Dashboard mode={mode} />} />
          <Route path="/config" element={<Configuration mode={mode} />} />
          <Route path="/docs/models" element={<Leaderboard />} />
          <Route path="/docs/architecture" element={<Architecture />} />
          <Route path="/learning/concepts" element={<Concepts />} />
          <Route path="/learning/glossary" element={<Glossary />} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </Layout>
    </HashRouter>
  );
};

export default App;
