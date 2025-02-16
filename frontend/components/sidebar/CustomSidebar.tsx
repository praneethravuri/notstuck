"use client";

import React from "react";

interface CustomSidebarProps {
  children: React.ReactNode;
}

const CustomSidebar = ({ children }: CustomSidebarProps) => {
  return (
    <div className="h-screen w-64 border-gray-800">
      <div className="h-full flex flex-col relative">
        <div className="flex-1 overflow-y-auto overflow-x-hidden scrollbar-thin scrollbar-track-transparent scrollbar-thumb-gray-800">
          <div className="space-y-4">
            {children}
          </div>
        </div>
        <div
          className="absolute top-0 left-0 right-0 h-4 bg-gradient-to-b from-stone-950 to-transparent pointer-events-none z-10"
          aria-hidden="true"
        />
        <div
          className="absolute bottom-0 left-0 right-0 h-4 bg-gradient-to-t from-stone-950 to-transparent pointer-events-none z-10"
          aria-hidden="true"
        />
      </div>
    </div>
  );
};

export default CustomSidebar;