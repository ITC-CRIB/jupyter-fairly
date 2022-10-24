import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';

import { ISettingRegistry } from '@jupyterlab/settingregistry';

import {
  // Dialog, 
  ICommandPalette, 
  // showDialog,
  InputDialog,
  // showErrorMessage,

} from '@jupyterlab/apputils';
import {
  IFileBrowserFactory,
  // FileBrowser,
  // FilterFileBrowserModel,
  
} from '@jupyterlab/filebrowser';

// import { DocumentManager } from '@jupyterlab/docmanager';

// import { DocumentRegistry } from '@jupyterlab/docregistry';


// Icons
import {
  addIcon,
  // closeIcon,
  // copyIcon,
  // cutIcon,
  // downloadIcon,
  // editIcon,
  // fileIcon,
  // folderIcon,
  // linkIcon,
  // markdownIcon,
  // newFolderIcon,
  // pasteIcon,
  // RankedMenu,
  // refreshIcon,
  // stopIcon,
  // textEditorIcon
} from '@jupyterlab/ui-components'

// import { showDialog} from '@jupyterlab/apputils';
// import { Dialog} from '@jupyterlab/apputils';
//examples with Dialog widget: https://www.programcreek.com/typescript/?api=@jupyterlab/apputils.Dialog


// import handlers from Jupyter Server extension
import { 
  initDataset 
} from './fairly-api';


/**
 * Initialization data for the jupyterfair extension.
 */
const newDataset: JupyterFrontEndPlugin<void> = {
  id: 'jupyterfair:newDataset',
  autoStart: true,
  requires : [ICommandPalette, IFileBrowserFactory],
  optional: [ISettingRegistry],
  activate: (app: JupyterFrontEnd, factory: IFileBrowserFactory, palette: ICommandPalette, settingRegistry: ISettingRegistry | null) => {
    console.log('JupyterLab extension jupyterfair widget is activated! 07-11');
    // console.log('IcommandPalette:', palette);

    // Declare command
    const commandCreateDataset = 'New Fairly Dataset';
   
    
    

    // add command to registry
    app.commands.addCommand(commandCreateDataset, {
      label: 'Create Fairly Dataset',
      isEnabled: () => true,
      isVisible: () => true,
      icon: addIcon,
      execute: () => {
        console.log(`Executed ${commandCreateDataset}`);
        // const browser = factory.tracker.currentWidget?.model.path;
        // console.log(browser)
        // const widget = tracker.currentWidget
        // const path = widget?.model.path;
        // console.log(path)
    
        InputDialog.getItem({
          title: 'Select format for new dataset\'s metadata',
          items: ['Default', '4TU.Research',  'Zenodo', 'Figshare']
        }).then(value => {
          console.log('item ' + value.value);
          // TODO: create manifest in current directory
          // Might find a way by analysing this code:
          // https://github.com/jupyterlab/jupyterlab/blob/621ae2a760331d08edceac31754633358a0c9018/packages/filebrowser-extension/src/index.ts#L823
          const root_path = './'
          try {
            initDataset(root_path , value.value);
          }
          catch(e){
            console.log("the error was caught!!");
          }

        });
      }
    });

  
    // Add to context menu
    app.contextMenu.addItem({
      command: commandCreateDataset,
      // matches anywhere in the filebrowser
      selector: '.jp-DirListing-content',
      rank: 100
    });
    // for examples: https://discourse.jupyter.org/t/add-entries-to-the-filebrowser-contextmenu/1651/2
  
  }
};

export default newDataset;
