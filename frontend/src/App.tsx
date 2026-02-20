import React from 'react';
import { Routes, Route } from 'react-router-dom';
import { Home } from './pages/Home/Home';
import { Game } from './pages/Game/Game';
import { Profile } from './pages/Profile/Profile';
import { Deposit } from './pages/Deposit/Deposit';
import { Withdraw } from './pages/Withdraw/Withdraw';

function App() {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/game" element={<Game />} />
      <Route path="/profile" element={<Profile />} />
      <Route path="/deposit" element={<Deposit />} />
      <Route path="/withdraw" element={<Withdraw />} />
    </Routes>
  );
}

export default App;
