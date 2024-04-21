import React from "react";
import "./home.css"

const Home = () => {
    return (
    <div className="container-fluid">
      <div className="container-fluid big-logo-container justify-content-center">
        <h1 className="big-logo h1">Attack Prediction Tool</h1>
      </div>
      <div className="container-fluid d-flex justify-content-center align-items-center sub-title">
        <h2 className="mb-0 display-4 sub-title text-primary">A tool to prevent attacks in your business </h2>
      </div>
      <div className="container-fluid align-items-center mouse"></div>
      <div className="container-fluid description hide">
        <div className="row justify-content-center align-items-center">
          <div className="col-lg-5 col-md-6 col-sm-8 justify-content-center text-center">
            <p>Dolor sit amet, consectetur adipisicing elit. Id maxime repellat repellendus porro voluptas laudantium similique eveniet quis perferendis beatae commodi sunt ullam provident dolorum doloribus esse accusamus dolores. Corrupti.</p>
            <p>Consectetur incidunt voluptatibus ipsa nisi esse eos deleniti repudiandae at quo sit praesentium nemo optio perspiciatis sequi quaerat voluptates minus reprehenderit doloremque accusamus et quisquam nesciunt sunt consequatur explicabo excepturi!</p>
          </div>
          <div className="row justify-content-center align-items-center text-center">
            <a className="text-decoration-none" href="searching_choice">
              <button type="button" className="btn btn-primary" aria-pressed="true">
                Get started
              </button>
            </a>
          </div>
          <div className="row justify-content-center align-items-center">
            <img src="../../assets/cyber.svg" className="cyber-img" alt="Cybersecurity Logo"/>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Home;