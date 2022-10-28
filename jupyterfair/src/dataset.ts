import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';

import { addIcon } from '@jupyterlab/ui-components'
import { Dialog, showDialog, InputDialog } from '@jupyterlab/apputils';
import { IFileBrowserFactory } from '@jupyterlab/filebrowser';
import { showErrorMessage } from '@jupyterlab/apputils';
import { downloadIcon } from '@jupyterlab/ui-components';

import { requestAPI } from './handler';
import { FairlyCloneForm } from './widgets/CloneForm';

// import handlers from Jupyter Server extension
// import { initDataset } from './fairly-api';

function initDataset(path: string, template?: any) {
  /**
   * Initializes a Fairly dataset
   * @param path - path to dataset root directory. Default to current path
   * @param template - alias of template for manifest.yalm
   */

  // name of the template for manifest.yalm
  let templateMeta = '';
  /* ./ is necessary becaucause defaultBrowser.Model.path
  * returns an empty string when fileBlowser is on the
  * jupyterlab root directory     
  */
  let rootPath = './'
  if(template === '4TU.Research' || template === 'Figshare') {
    templateMeta = 'figshare';
  }
  else if (template === 'Zenodo'){
    templateMeta = 'zenodo'
  }
  else if (template == null || template === 'Default'){
    templateMeta = 'default'
  }

  console.log(rootPath.concat(path))
  requestAPI<any>('newdataset', {
    method: 'POST', 
    body: JSON.stringify({
      path: rootPath.concat(path),  // TODO: this might not work in Windows
      template: templateMeta
    })
  }) 
  .then(data => {
    console.log(data);
  })
  .catch(reason => {
    console.error(
      `${reason}`
    );
    // show error when manifest.yalm already exist in rootPath
    showErrorMessage("Error: Has the dataset been initilized already?", reason)
  });
}

export const cloneDatasetCommandPlugin: JupyterFrontEndPlugin<void> = {
  id: 'jupyterfair:clone',
  requires: [IFileBrowserFactory],
  autoStart: true,
  activate: (
    app: JupyterFrontEnd,
    fileBrowserFactory: IFileBrowserFactory
  ) => {
    console.log("cloneDatasetCommandPlugin activated!!");
    const fileBrowser = fileBrowserFactory.defaultBrowser;
    const fileBrowserModel = fileBrowser.model;

    const cloneDatasetCommand = "cloneDatasetCommand";
    app.commands.addCommand(cloneDatasetCommand, {
      label: 'Clone a Dataset',
      isEnabled: () => true,
      isVisible: () => true,
      icon: downloadIcon,
      execute:async () => {
        const result = await showDialog({
          title: 'Clone a Dataset',
          body: new FairlyCloneForm(),
          buttons: [
            Dialog.cancelButton({ label: 'Cancel'}),
            Dialog.okButton({ label: 'Clone'})
          ]
        });

        if (result.button.accept && result.value) {
          console.log('accepted');
          await fileBrowserModel.refresh();
        }
      } 
    });

    app.contextMenu.addItem({
      command: cloneDatasetCommand,
      // matches anywhere in the filebrowser
      selector: '.jp-DirListing-content',
      rank: 106
    });

  }
};

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
          title: 'Select template for dataset\'s metadata',
          items: ['', 'Default', '4TU.Research',  'Zenodo', 'Figshare'],
          okLabel: 'Create',
        });
        
        // initialize dataset when accept button is clicked and 
        // vaule for teamplate is not null
        if (metadataTemplate.button.accept && metadataTemplate.value) {
          console.log( `the path is: ${fileBrowserModel.path}` );
          initDataset(fileBrowserModel.path , metadataTemplate.value);
          await fileBrowserModel.refresh();
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