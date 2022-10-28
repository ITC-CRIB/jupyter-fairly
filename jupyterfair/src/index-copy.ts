import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';

// import { ISettingRegistry } from '@jupyterlab/settingregistry';

// import {
//   // Dialog, 
//   ICommandPalette, 
//   // showDialog,
// } from '@jupyterlab/apputils';
import { IFileBrowserFactory } from '@jupyterlab/filebrowser';


/**
 * Initialization data for the jupyterfair extension.
 */

export const pathCommandPlugin: JupyterFrontEndPlugin<void> = {
  id: 'jupyterfair:path',
  requires: [IFileBrowserFactory],
  autoStart: true,
  activate: (
    app: JupyterFrontEnd,
    fileBrowserFactory: IFileBrowserFactory
  ) => {
    console.log("pathCommandPlugin activated!!");
    const fileBrowser = fileBrowserFactory.defaultBrowser;
    const fileBrowserModel = fileBrowser.model;

    // TODO: the plugin start without error, but the model.path is an empty string for root-path (path where jupyter was started.)
    const pathCommand = "path command"
    app.commands.addCommand(pathCommand, {
      label: 'Path Command',
      isEnabled: () => true,
      isVisible: () => true,
      execute: () => {

        // return relative path w.r.t. jupyter root path.
        // root-path = empty string.
        console.log( `the path is: ${fileBrowserModel.path}` );
      }
    });

    app.contextMenu.addItem({
      command: pathCommand,
      // matches anywhere in the filebrowser
      selector: '.jp-DirListing-content',
      rank: 105
    });
  }
};



///
// function initDataset(rootPath:string, template: any) {
//   requestAPI<any>('newdataset', {
//     method: 'POST', 
//     body: JSON.stringify({
//       path: rootPath, 
//       template: template
//     })
//   }) // This is how to query the api-url
//   .then(data => {
//     console.log(data);
//   })
//   .catch(reason => {
//     console.error(
//       `The jupyterfair server extension appears to be missing.\n${reason}`
//     );
//   });
// }

// const fbModel = new FilterFileBrowserModel({ manager: docManager});

    // const fbWidget = new FileBrowser({
    //   id: 'filebrowser',
    //   model: 
    // };

    
    // const browser = factory.tracker.currentWidget;
    
    // console.log(browser);
    // const basePath = factory.defaultBrowser.model.path;
    // // const basePath = factory.tracker.;
    // console.log(`workspace: ${basePath}`);
    // const {tracker} = factory;