import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';

/**
 * Initialization data for the jupyter-py5 extension.
 */
const plugin: JupyterFrontEndPlugin<void> = {
  id: 'jupyter-py5:plugin',
  description: 'py5 Jupyter tools',
  autoStart: true,
  activate: (app: JupyterFrontEnd) => {
    console.log('JupyterLab extension jupyter-py5 is activated!');
  }
};

export default plugin;
