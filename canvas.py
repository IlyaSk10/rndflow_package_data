from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np


class Canvas(FigureCanvas):
    def __init__(self, widget, ui, fig_func_params, fig_id='0', **kwargs):
        self.__dict__.update(kwargs)
        self.ui = ui
        self.fig = None
        if hasattr(self, f'fig{fig_id}'):
            getattr(self, f'fig{fig_id}')(**fig_func_params)  # drawing figure by fig_id
        super().__init__(self.fig, **kwargs)
        self.setParent(widget)
        self.toolbar = NavigationToolbar(self, widget)
        self.ui.clear_layout(widget.layout())
        widget.layout().addWidget(self.toolbar)
        widget.layout().addWidget(self)
        if widget is None:
            plt.show()

    def fig0(self, sz, **kwargs):
        #fig0 : plot f[SZ]
        #SZ is 2d array, x - sensor number, y - registered signal
        #half of sensors is 'forward', half is 'backward'
        self.fig, ax = plt.subplots(figsize=(6,6), constrained_layout=True)
        im = ax.imshow(sz,vmin=-0.6,vmax=0.6)
        ax.set_aspect(0.6)
        ax.tick_params(labelsize=10)
        ax.set_xlim(0, self.fig.bbox.width)
        ax.set_ylim(0, self.fig.bbox.height)
        cbar=self.fig.colorbar(im,fraction=0.05)
        cbar.ax.tick_params(labelsize=10)
        ax.set_xlabel('Sensors',fontsize=12)
        ax.set_ylabel('Samples',fontsize=12)
        ax.set_title('SEGY')
        self.fig.canvas.draw_idle()

    def fig1(self, diff_sz, **kwargs):
        #fig1 : plot diff_SZ
        #uniform for this segy, nothing special
        #it means that signals don't have any spikes
        self.fig, ax = plt.subplots(figsize=(6,6), constrained_layout=True)
        im = ax.imshow(diff_sz,vmin=-0.05,vmax=0.05)
        ax.set_aspect(0.6)
        ax.tick_params(labelsize=10)
        cbar=self.fig.colorbar(im,fraction=0.05)
        cbar.ax.tick_params(labelsize=10)
        ax.set_xlabel('Sensors',fontsize=12)
        ax.set_ylabel('Samples',fontsize=12)
        ax.set_title('derivative SEGY')
        self.fig.canvas.draw_idle()

    def fig2(self, diff_sz, **kwargs):
        #fig2 : plot signals derivatives of 17 sensor
        self.fig, ax = plt.subplots(figsize=(10,5), constrained_layout=True)
        ax.plot((diff_sz[0:2600,17]),label='forward')
        ax.plot((diff_sz[0:2600,diff_sz.shape[1]-17-1]),label='backward')
        ax.tick_params(labelsize=12)
        ax.set_xlabel('Samples',fontsize=12)
        ax.set_title('plot 17 sensor')
        ax.legend()
        self.fig.canvas.draw_idle()

    def fig2w(self, diff_SZ, sensor_num=17, **kwargs):
        #fig2w : plot spectrum of the signal derivatives of 17 sensor
        x = diff_SZ[0:2600, sensor_num]
        nn = len(x)
        xfreq = np.fft.fftfreq(nn, 1/fd)
        xw = np.fft.fft(x)
        self.fig, ax = plt.subplots(figsize=(10,5), constrained_layout=True)
        ax.plot(np.fft.fftshift(xfreq), np.abs(np.fft.fftshift(xw)), label = 'forward')
        #ax.plot((diff_SZ[0:2600,diff_SZ.shape[1]-17-1]),label='backward')
        ax.tick_params(labelsize=12)
        ax.set_xlabel('Frequency (Hz)',fontsize=12)
        ax.set_title('spectrum 17 sensor (forward)')
        ax.set_xlim([0,100])
        ax.legend()
        self.fig.canvas.draw_idle()

    def fig6(self, median_filter_res, **kwargs):
        # median filter
        self.fig, ax = plt.subplots(figsize=(6,5), constrained_layout=True)
        im = ax.imshow(median_filter_res,vmin=-0.05,vmax=0.05)
        ax.set_aspect(0.6)
        ax.tick_params(labelsize=10)
        cbar=self.fig.colorbar(im,fraction=0.05)
        cbar.ax.tick_params(labelsize=10)
        ax.set_xlabel('Sensors',fontsize=12)
        ax.set_ylabel('Samples',fontsize=12)
        ax.set_title('median filtration')
        self.fig.canvas.draw_idle()

    def fig7a(self, sfreq, samp, bpf_res_w, **kwargs):
        #fig7a : spectrum after band pass filter
        self.fig, ax = plt.subplots(figsize=(6,5), constrained_layout=True)
        im = ax.contourf(sfreq, samp, np.abs(bpf_res_w).T, 30)#,vmin=-0.01,vmax=0.01)
        ax.set_aspect(0.6)
        ax.tick_params(labelsize=10)
        cbar=self.fig.colorbar(im,fraction=0.05)
        cbar.ax.tick_params(labelsize=10)
        ax.set_xlabel('Frequency (Hz)',fontsize=12)
        ax.set_ylabel('Sensor number',fontsize=12)
        ax.set_title('band pass filtration')
        # plt.savefig("myImagePDF.png", format="png",bbox_inches='tight')
        self.fig.canvas.draw_idle()

    def fig8(self, ndimage, bpf_res, **kwargs):
        # median filter 2d plot standard deviation
        self.fig, ax = plt.subplots(figsize=(6,5), constrained_layout=True)
        ax.plot(ndimage.median_filter(np.std(bpf_res,axis=0)[1400:2000], size=5))
        ax.set_xticks([i for i in range(0,700,100)],[i for i in range(1400,2100,100)])
        ax.tick_params(labelsize=12)
        ax.set_xlabel('Sensors',fontsize=12)
        ax.set_title('Initial std')
        ax.legend()
        self.fig.canvas.draw_idle()

    def fig7b(self, samp, sfreq, spectrum_before_bpf, nyq, **kwargs):
        #fig7b : spectrum before band pass filter
        self.fig, ax = plt.subplots(figsize=(6,5), constrained_layout=True)
        #ax = fig7b.gca()
        im = ax.contourf(samp,sfreq,np.abs(spectrum_before_bpf), 30)#,vmin=-0.01,vmax=0.01)
        ax.set_aspect(0.6)
        ax.tick_params(labelsize=10)
        cbar=self.fig.colorbar(im,fraction=0.05)
        cbar.ax.tick_params(labelsize=10)
        ax.set_ylabel('Frequency (Hz)',fontsize=12)
        ax.set_xlabel('Sensor number',fontsize=12)
        ax.set_title('band pass filtration')
        ax.set_ylim([0,nyq])
        # plt.savefig("myImagePDF.png", format="png",bbox_inches='tight')
        self.fig.canvas.draw_idle()

    def fig9(self, sz_norm, **kwargs):
        # median transform with normalization
        self.fig, ax = plt.subplots(figsize=(6,5), constrained_layout=True)
        im = ax.imshow(sz_norm,vmin=-0.01,vmax=0.01)
        ax.set_aspect(0.6)
        ax.tick_params(labelsize=10)
        cbar=self.fig.colorbar(im,fraction=0.05)
        cbar.ax.tick_params(labelsize=10)
        ax.set_xlabel('Sensors',fontsize=12)
        ax.set_ylabel('Samples',fontsize=12)
        ax.set_title('Noise level normalization')
        self.fig.canvas.draw_idle()

    def fig10(self, sz_norm, **kwargs):
        self.fig, ax = plt.subplots(figsize=(4,5), constrained_layout=True)
        ax.plot(np.std(sz_norm,axis=0))
        ax.set_title('Noise level after normalization')
        self.fig.canvas.draw_idle()

    def fig11(self, a, **kwargs):
        # plot B/C
        self.fig, ax = plt.subplots(figsize=(6,6), constrained_layout=True)
        im = ax.imshow(a,vmin=0,vmax=2)
        ax.set_aspect(10)
        ax.tick_params(labelsize=14)
        cbar=self.fig.colorbar(im,fraction=0.025)
        cbar.ax.tick_params(labelsize=14)
        ax.set_xlabel('Number of sensors',fontsize=14)
        ax.set_title('101/51')
        self.fig.canvas.draw_idle()

    def fig12(self, samp, sfreq, spectrum_shifted, nyq, **kwargs):
        # spectrum plot (in human-readable form)
        self.fig, ax = plt.subplots(figsize=(10,10), constrained_layout=True)
        im = ax.contourf(samp, sfreq, spectrum_shifted,30, vmin=0.2,vmax=8)
        ax.set_aspect(0.7)
        ax.tick_params(labelsize=10)
        cbar=self.fig.colorbar(im, fraction=0.025)
        cbar.ax.tick_params(labelsize=10)
        ax.set_xlabel('Sensors',fontsize=12)
        ax.set_ylabel('Frequency (Hz)',fontsize=12)
        ax.set_title('spectrum')
        ax.set_ylim([0,nyq])
        #ax.set_yticks([i for i in range(0,naikvist_sample,100)],[round(i*fd/SZ_norm.shape[0]) for i in range(0,naikvist_sample,100)])
        self.fig.canvas.draw_idle()

    def fig13(self, samp, sfreq, spect_trans_shifted, **kwargs):
        # plot spectrum of transformed signal (in human-readable form)
        self.fig, ax = plt.subplots(figsize=(10,10), constrained_layout=True)
        im = ax.contourf(samp, sfreq, spect_trans_shifted, 30,vmin=0,vmax=8)
        ax.set_aspect(0.7)
        ax.tick_params(labelsize=10)
        cbar=self.fig.colorbar(im,fraction=0.025)
        cbar.ax.tick_params(labelsize=10)
        ax.set_xlabel('Number of sensors',fontsize=12)
        ax.set_ylabel('Frequency (Hz)',fontsize=12)
        ax.set_title('spectrum transform signal')
        ax.set_ylim([0,nyq])
        #ax.set_yticks([i for i in range(0,naikvist_sample,100)],[round(i*fd/SZ_norm.shape[0]) for i in range(0,naikvist_sample,100)])
        self.fig.canvas.draw_idle()

    def fig14(self, samp, sfreq, nf, spect_sz_upd, **kwargs):
        # plot normalization to lower freq
        self.fig, ax = plt.subplots(figsize=(10,10), constrained_layout=True)
        im = ax.contourf(samp, sfreq, nf.fftshift(spect_sz_upd,axes=0),30,vmin=0,vmax=2)
        ax.set_aspect(0.7)
        ax.tick_params(labelsize=10)
        cbar=self.fig.colorbar(im,fraction=0.025)
        cbar.ax.tick_params(labelsize=10)
        ax.set_xlabel('Number of sensors',fontsize=12)
        ax.set_ylabel('Frequency (Hz)',fontsize=12)
        ax.set_title('normalization to lower freq')
        ax.set_ylim([0,nyq])
        #ax.set_yticks([i for i in range(0,naikvist_sample,100)],[round(i*fd/SZ_norm.shape[0]) for i in range(0,naikvist_sample,100)])
        self.fig.canvas.draw_idle()

    def fig15(self, transform_sz_upd, **kwargs):
        # plot transform_SZ_upd
        self.fig, ax = plt.subplots(figsize=(10,10), constrained_layout=True)
        im = ax.imshow(transform_sz_upd,vmin=-0.005,vmax=0.005)
        ax.set_aspect(1)
        ax.tick_params(labelsize=10)
        cbar=self.fig.colorbar(im,fraction=0.05)
        cbar.ax.tick_params(labelsize=10)
        ax.set_xlabel('Sensors',fontsize=12)
        ax.set_title('Transform SZ upd')
        #plt.savefig("myImagePDF.png", format="png",bbox_inches='tight')
        self.fig.canvas.draw_idle()
