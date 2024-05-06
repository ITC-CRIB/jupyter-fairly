import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';

import { ISettingRegistry } from '@jupyterlab/settingregistry';

import { requestAPI } from './handler';

/**
 * Initialization data for the jupyter-fairly extension.
 */
const plugin: JupyterFrontEndPlugin<void> = {
  id: 'jupyter-fairly:plugin',
  description: 'A JupyterLab extension for seamless integration of Jupyter-based research environments and research data repositories',
  autoStart: true,
  optional: [ISettingRegistry],
  activate: (app: JupyterFrontEnd, settingRegistry: ISettingRegistry | null) => {
    console.log('JupyterLab extension jupyter-fairly is activated!');

    if (settingRegistry) {
      settingRegistry
        .load(plugin.id)
        .then(settings => {
          console.log('jupyter-fairly settings loaded:', settings.composite);
        })
        .catch(reason => {
          console.error('Failed to load settings for jupyter-fairly.', reason);
        });
    }

    requestAPI<any>('get-example')
      .then(data => {
        console.log(data);
      })
      .catch(reason => {
        console.error(
          `The jupyter_fairly server extension appears to be missing.\n${reason}`
        );
      });
  }
};

export default plugin;
