"use client";
import React from "react";

interface CustomSidebarProps {
  children: React.ReactNode;
}

const CustomSidebar = ({ children }: CustomSidebarProps) => {
  return (
    <div className="h-screen w-64 border-gray-800 overflow-hidden">
      <div className="h-full flex flex-col relative">
        <div className="flex-1 overflow-y-auto overflow-x-hidden">
          <div>{children}</div>
        </div>
      </div>
    </div>
  );
};

export default CustomSidebar;