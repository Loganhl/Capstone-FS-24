import React from "react";
import { Navbar } from "react-bootstrap";
import { DiGithubBadge } from 'react-icons/di'

const Footer = ({ theme }) => {
  const openGithub = () => {
    window.open("https://github.com/Loganhl/Capstone-FS-24");
  };

  return (
    <Navbar
      sticky="bottom"
      className={`navbar-${theme} bg-body-${theme} d-flex justify-content-center`}
      variant={theme === "light" ? "light" : "dark"}
    >
      <button
        onClick={openGithub}
        style={{
          background: "none",
          border: "none",
          padding: 0,
          cursor: "pointer",
          color: "inherit",
        }}
        aria-label="GitHub Repository"
      >
        <DiGithubBadge size={30} />
      </button>
    </Navbar>
  );
};

export default Footer;
