import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';

import { ISettingRegistry } from '@jupyterlab/settingregistry';
import { ICommandPalette,} from '@jupyterlab/apputils';

import { 
  createDatasetCommandPlugin,
  cloneDatasetCommandPlugin, 
} from './dataset';
import {editMetadataPlugin} from './metadata'
import { uploadDatasetPlugin} from './upload';
import { FairlyMenuPlugin } from './menu';


/**
 *  Activate jupyter-fairly extension.
 */
const plugin: JupyterFrontEndPlugin<void> = {
  id: 'jupyter-fairly:plugin',
  autoStart: true,
  requires : [ICommandPalette],
  optional: [ISettingRegistry],
  activate: (app: JupyterFrontEnd,
    palette: ICommandPalette, 
    settingRegistry: ISettingRegistry | null) => {
    
      console.log('jupytefair is activated!!');
      
  }
};


export default [
  plugin, 
  createDatasetCommandPlugin, 
  editMetadataPlugin, 
  uploadDatasetPlugin,
  cloneDatasetCommandPlugin,
  FairlyMenuPlugin,
];

//Todo: add new tab to left pannel
// example: https://github.com/jupyterlab/extension-examples/tree/master/widgets
