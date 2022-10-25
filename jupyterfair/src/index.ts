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
  editIcon,
  fileUploadIcon,
  // textEditorIcon,
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
    const commandCreateDataset = 'fairly: create';
   
    
    

    // add command to registry
    app.commands.addCommand(commandCreateDataset, {
      label: 'Create Fairly Dataset',
      isEnabled: () => true,
      isVisible: () => true,
      icon: addIcon,
      execute: () => {
        console.log(`Executed ${commandCreateDataset}`);
    
        InputDialog.getItem({
          title: 'Select format for new dataset\'s metadata',
          items: ['Default', '4TU.Research',  'Zenodo', 'Figshare'],
          okLabel: 'Create',
        }).then(value => {
          console.log('item ' + value.value);
          // TODO: create manifest in current directory
          // Might find a way by analysing this code:
          // https://github.com/jupyterlab/jupyterlab/blob/621ae2a760331d08edceac31754633358a0c9018/packages/filebrowser-extension/src/index.ts#L823
          const root_path = './'
          // TODO: dataset is initialized when cancel is clicked.
          initDataset(root_path , value.value);

        });
      }
    });
  
    // Add to context menu
      // for examples: https://discourse.jupyter.org/t/add-entries-to-the-filebrowser-contextmenu/1651/2
    app.contextMenu.addItem({
      command: commandCreateDataset,
      // matches anywhere in the filebrowser
      selector: '.jp-DirListing-content',
      rank: 100
    });

    const commandEditMetadata = 'fairly:edit-metadata'
    // Opens the manifest.yalm file in the file editor
    app.commands.addCommand(commandEditMetadata, {
      label: 'Edit Dataset Metadata',
      isEnabled: () => true,
      isVisible: () => true,
      icon: editIcon,
      execute: () => {
        console.log(`Executed ${commandEditMetadata}`);
      }
    });

    app.contextMenu.addItem({
      command: commandEditMetadata,
      // matches anywhere in the filebrowser
      selector: '.jp-DirListing-content',
      rank: 101
    });

    const commandArchiveDataset = 'fairly:archive'
    // Archives dataset to selected Data repository
    app.commands.addCommand(commandArchiveDataset, {
      label: 'Archive Dataset',
      isEnabled: () => true,
      isVisible: () => true,
      icon: fileUploadIcon,
      execute: () => {
        console.log(`Executed ${commandArchiveDataset}`);
      }
    });

    app.contextMenu.addItem({
      command: commandArchiveDataset,
      // matches anywhere in the filebrowser
      selector: '.jp-DirListing-content',
      rank: 102
    });
  
  
  }
};

export default newDataset;
