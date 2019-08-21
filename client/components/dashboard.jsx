import React from 'react';

const Dashboard = () => {
    return(
        <div className="row">
        <h3 className="col-12">Welcome to SavvyBiz Practical Test</h3>
        <div className="col-12">
            <strong>Objectives:</strong>
            <p>You are required to prove your ability do ReactJS on Django (Testing is a plus).
                Having the ability to do Test Driven Development with optimal coverage will be an added advantage </p>

            <strong>Task:</strong>
            <p>This project uses Django forms and Django default templates to create, edit and view Company and Company is a model defined in the core app.<br />
                You are required to implement ReactJS equivalent of the current Django templates retaining all the functionalities that currently exists.
                <i>It will be a plus to have TDD </i></p>

        </div>

        <p></p>
    </div>
    )
}

export default Dashboard;