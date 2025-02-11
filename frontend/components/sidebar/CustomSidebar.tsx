// CustomSidebar.tsx
"use client";
import React from "react";

interface CustomSidebarProps {
  children: React.ReactNode;
}

const CustomSidebar = ({ children }: CustomSidebarProps) => {
  return (
    <div className="h-screen bg-stone-950 flex flex-col">
      {/* Logo Section */}


      {/* Render the passed-in children */}
      <div className="h-screen flex flex-col justify-between overflow-y-auto">
        {children}
      </div>
    </div>
  );
};

export default CustomSidebar;
