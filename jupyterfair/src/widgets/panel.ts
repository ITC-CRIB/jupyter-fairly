import { JupyterFrontEndPlugin, JupyterFrontEnd } from "@jupyterlab/application";
import { Panel, Widget } from "@lumino/widgets";
import { tabIcon } from "@jupyterlab/ui-components";
import { ReactWidget } from "@jupyterlab/apputils";

 

export const leftSidePanel: JupyterFrontEndPlugin<void> = {
    id: 'jupyterfair: left-panel',
    autoStart: true,
    activate:async (app: JupyterFrontEnd) => {
        addLeftPanel(app);
        
    }
};

function addLeftPanel (app: any) {
    const panel = new Panel();
    panel.id = 'example-panel';
    panel.title.icon = tabIcon;


    panel.addWidget(new Widget());
    app.shell.add(panel, 'left', {rank: 4});
}

// export class ExampleWidget extends ReactWidget {
//     render (): JSX.Element {
//         return (
//             <ExampleComponent />
//         );
//     }
// };


// function ExampleComponent() {
//     return(
//         <body id="main">
//             <div> <h2>Hello</h2></div>
//         </body>
//     );
// };