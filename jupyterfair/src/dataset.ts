import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';

import{addIcon} from '@jupyterlab/ui-components'
import { InputDialog } from '@jupyterlab/apputils';
import { IFileBrowserFactory } from '@jupyterlab/filebrowser';

// import handlers from Jupyter Server extension
import { initDataset } from './fairly-api';

export const createDatasetCommandPlugin: JupyterFrontEndPlugin<void> = {
  id: 'jupyterfair:create-dataset',
  requires: [IFileBrowserFactory],
  autoStart: true,
  activate: (
    app: JupyterFrontEnd,
    fileBrowserFactory: IFileBrowserFactory
  ) => {
    console.log("createDatasetCommandPlugin activated!!");
    const fileBrowser = fileBrowserFactory.defaultBrowser;
    const fileBrowserModel = fileBrowser.model;

    // TODO: the plugin start without error, but the model.path is an empty string for root-path (path where jupyter was started.)
    const createDatasetCommand = "createDatasetCommand"
    app.commands.addCommand(createDatasetCommand, {
      label: 'Create Fairly Dataset',
      isEnabled: () => true,
      isVisible: () => true,
      icon: addIcon,
      execute: async () => {

        // return relative path w.r.t. jupyter root path.
        // root-path = empty string.
        console.log( `the path is: ${fileBrowserModel.path}` );

        let metadataTemplate = await InputDialog.getItem({
          title: 'Select format for new dataset\'s metadata',
          items: ['', 'Default', '4TU.Research',  'Zenodo', 'Figshare'],
          okLabel: 'Create',
        });
        
        // initialize dataset when accept button is clicked and 
        // vaule for teamplate is not null
        if (metadataTemplate.button.accept && metadataTemplate.value) {
          console.log( `the path is: ${fileBrowserModel.path}` );
          initDataset(fileBrowserModel.path , metadataTemplate.value);
        } else{
          console.log('rejected')
          return
        }

      }
    });

    app.contextMenu.addItem({
      command: createDatasetCommand,
      // matches anywhere in the filebrowser
      selector: '.jp-DirListing-content',
      rank: 100
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