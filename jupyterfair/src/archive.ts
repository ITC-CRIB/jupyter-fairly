import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';

import {
  InputDialog
} from '@jupyterlab/apputils';

import { 
  IFileBrowserFactory 
} from '@jupyterlab/filebrowser';

// Icons
import {
  fileUploadIcon,
} from '@jupyterlab/ui-components';

/**
 * Initialization data for the jupyterfair extension.
 */

export const archiveDatasetPlugin: JupyterFrontEndPlugin<void> = {
  id: 'jupyterfair:archive',
  requires: [IFileBrowserFactory],
  autoStart: true,
  activate: (
    app: JupyterFrontEnd,
    fileBrowserFactory: IFileBrowserFactory
  ) => {
    console.log("archiveDatasetPlugin activated!!");
    const fileBrowser = fileBrowserFactory.defaultBrowser;
    const fileBrowserModel = fileBrowser.model;

    // TODO: the plugin start without error, but the model.path is an empty string for root-path (path where jupyter was started.)
    const archiveDatasetCommand = "archiveDataset"
    app.commands.addCommand(archiveDatasetCommand, {
      label: 'Archive Dataset',
      isEnabled: () => true,
      isVisible: () => true, // activate only when current directory contains a manifest.yalm
      icon: fileUploadIcon,
      execute: async() => {

        // return relative path w.r.t. jupyter root path.
        // root-path = empty string.
        console.log( `the path is: ${fileBrowserModel.path}` );

        let targetRepository = await InputDialog.getItem({
          title: 'Select Data Repository',
          items: ['4TU.ResearchData',  'Zenodo', 'Figshare'],
          okLabel: 'Continue',
        });
        
        // initialize dataset when accept button is clicked and 
        // vaule for teamplate is not null
        if (targetRepository.button.accept && targetRepository.value) {
          
          let confirmAction = await InputDialog.getBoolean({
            title: 'Do you want to archive the dataset?',
            label: `Yes, upload metadata and files to ${targetRepository.value}`
          });

          if (confirmAction.button.accept){
            console.log ('archive dataset');
          }else {
            console.log('do not archive');
            return
          };

        } else{
          console.log('rejected')
          return
        }

      }
    });

    app.contextMenu.addItem({
      command: archiveDatasetCommand,
      // matches anywhere in the filebrowser
      selector: '.jp-DirListing-content',
      rank: 102
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