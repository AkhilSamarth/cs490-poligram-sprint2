import React from 'react'
import { BrowserRouter, Route, Switch } from 'react-router-dom';
import Dictionary from './Components/Dictionary'
import Home from './Components/Home';
import Navigation from './Components/Navigation';
import Quiz from './Components/Quiz';

const Content = () => {

    return (
        <BrowserRouter>
            <div>
                <Navigation />
                <Switch>
                    <Route path="/" component={Home} exact/>
                    <Route path="/Dictionary" component={Dictionary}/>
                    <Route path="/Quiz" component={Quiz} />
                    <Route component={Error}/>
                </Switch>
            </div>
        </BrowserRouter>
    );
};

export default Content;
