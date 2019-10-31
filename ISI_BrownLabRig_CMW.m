% Intrinsic Signal Imaging - Brown lab Rig
%Requirements:
%   -one Arduino Uno + Matlab_Arduino package (Environment>AddOns>Get
%   Hardware Support Packages)
%   -Piezo (Thorlabs XXX)
%   -Signal generator (XXXX)
%   -Camera (Thorlab XXX)
%   -MicroManager + Config (camera specific) + Java pluggins (instructions
%   at https://micro-manager.org/wiki/Matlab_Configuration)
%   -LED ~450nm
%   -LED ~?

%% Set up 
%Open communication with Arduino
Arduino=arduino('com4', 'uno');

%Load Camera java pluggins
import mmcorej.*;
mmc = CMMCore; %Camera object
%MicroManager needs to be closed for this to work
mmc.loadSystemConfiguration ('C:\Program Files\Micro-Manager-2.0gamma\MMConfig_demo.cfg'); %You can create a Config file in MicroManager for you specific camera (Devices>Hardware Configuration Wizard>...)
mmc.setExposure(1000) %Set exposure, for ISI we do 1000msec per acquisition
Reps=20; %number of times you want to repeat the Stim/Acquire loop

%% Blood vessel image 1
mmc.snapImage();
img = mmc.getImage();  % returned as a 1D array of signed integers in row-major order
width = mmc.getImageWidth();
height = mmc.getImageHeight();
if mmc.getBytesPerPixel == 2
    pixelType = 'uint16';
else
    pixelType = 'uint8';
end
img = typecast(img, pixelType);      % pixels must be interpreted as unsigned integers
img = reshape(img, [width, height]); % image should be interpreted as a 2D array
img = transpose(img);                % make column-major order for MATLAB
imshow(img);
Vessels1=img; %Store image
%add save function here*
%% Execution
All_img=cell(1,Reps);
for i=1:Reps
    
    %Acquire pre-pulse image
    mmc.snapImage();
    imgpre = mmc.getImage();  % returned as a 1D array of signed integers in row-major order
    width = mmc.getImageWidth();
    height = mmc.getImageHeight();
    if mmc.getBytesPerPixel == 2
        pixelType = 'uint16';
    else
        pixelType = 'uint8';
    end
    imgpre = typecast(imgpre, pixelType);      % pixels must be interpreted as unsigned integers
    imgpre = reshape(imgpre, [width, height]); % image should be interpreted as a 2D array
    imgpre = transpose(imgpre); 
    %imgpre_all{i}=imgpre; %store each image separately in a growing array
    % make column-major order for MATLAB
    %imshow(img);
    
    %Pulse DDS 
    writeDigitalPin(Arduino,'D12',1);
    pause(0.5) %a 10msec pulse is sufficient to launch th signal generator. Control the pulse length there 
    % it should be about 5seconds
    writeDigitalPin(Arduino,'D12', 0);
    disp('hello')
    
    %Wait
    pause(15) %this includes the 5sec the DDS will be stimulating the whisker and the 15sec to let the blood flow before acquiring the image
    
    %Acquire stimulation image 
    mmc.snapImage();
    imgstim = mmc.getImage();  % returned as a 1D array of signed integers in row-major order
    width = mmc.getImageWidth();
    height = mmc.getImageHeight();
    if mmc.getBytesPerPixel == 2
        pixelType = 'uint16';
    else
        pixelType = 'uint8';
    end
    imgstim = typecast(imgstim, pixelType);      % pixels must be interpreted as unsigned integers
    imgstim = reshape(imgstim, [width, height]); % image should be interpreted as a 2D array
    imgstim = transpose(imgstim); 
    %imgstim_all{i}=imgstim; %store each image separately in a growing array
    % make column-major order for MATLAB
    %imshow(img);
    All_img{i}=double(imgstim-imgpre);
end


%% Optimize time between stimulus and img capture

mmc.setExposure(1000)

% Acquire pre-stim image
    mmc.snapImage();
    imgpre = mmc.getImage();  % returned as a 1D array of signed integers in row-major order
    width = mmc.getImageWidth();
    height = mmc.getImageHeight();
    if mmc.getBytesPerPixel == 2
        pixelType = 'uint16';
    else
        pixelType = 'uint8';
    end
    imgpre = typecast(imgpre, pixelType);      % pixels must be interpreted as unsigned integers
    imgpre = reshape(imgpre, [width, height]); % image should be interpreted as a 2D array
    imgpre = transpose(imgpre); 
    
 %Pulse DDS
  writeDigitalPin(Arduino,'D12',1);
    pause(0.5) %a 10msec pulse is sufficient to launch th signal generator. Control the pulse length there 
    % it should be about 5seconds
    writeDigitalPin(Arduino,'D12', 0);
    disp('hello')
    
 %Wait
 pause(5) %DDS will stimulate whisker for 5 seconds
 
 %Acquire image every second after stimulus (make sure exposure is set to
 %1000)
 All_img=cell(1,30);
for i=1:30
    mmc.snapImage();
    imgstim = mmc.getImage();  % returned as an 1D array of signed integers in row-major order
    width = mmc.getImageWidth();
    height = mmc.getImageHeight();
    if mmc.getBytesPerPixel == 2
        pixelType = 'uint16';
    else
        pixelType = 'uint8';
    end
    imgstim = typecast(imgstim, pixelType);      % pixels must be interpreted as unsigned integers
    imgstim = reshape(imgstim, [width, height]); % image should be interpreted as a 2D array
    imgstim = transpose(imgstim); % make column-major order for MATLAB
    imgstim_all{i}=imgstim;
    All_img{i}=double(imgstim-imgpre);

end

for j=1:30
    figure(j)
    imshow(All_img{1,j})
end







%% For subtraction
Sum_All=double(All_img{1});
for j=2:5
    Sum_All=double(All_img{j})+Sum_All;
end
imshow(zscore(Sum_All/(5*255)))
Sum_Allcrop=(Sum_All(200:900,200:900))
imshow(Sum_Allcrop)

%% Average and then subtract
% make sure to comment out last line of execution if using this method

%average the pre-stimulation data
imgpre_sum=double(imgpre_all{1});
for j=2:Reps
    imgpre_sum=double(imgpre_all{j})+(imgpre_sum);
    disp('pre')
end
imgpre_avg=imgpre_sum/Reps;

%average post-stimulation data
imgstim_sum=double(imgstim_all{1});
for j=2:Reps
    imgstim_sum=double(imgstim_all{j})+(imgstim_sum);
    disp('post')
end 
imgstim_avg=imgstim_sum/Reps;
%plot difference of stimulation and pre-stimulation
imshow(imgstim_avg-imgpre_avg)

imshow(zscore(imgstim_avg-imgpre_avg))

%% Blood vessel image 2
mmc.snapImage();
img = mmc.getImage();  % returned as a 1D array of signed integers in row-major order
width = mmc.getImageWidth();
height = mmc.getImageHeight();
if mmc.getBytesPerPixel == 2
    pixelType = 'uint16';
else
    pixelType = 'uint8';
end
img = typecast(img, pixelType);      % pixels must be interpreted as unsigned integers
img = reshape(img, [width, height]); % image should be interpreted as a 2D array
img = transpose(img);                % make column-major order for MATLAB
imshow(img);
Vessels2=img; %Store image

imshow(Vessels1-Vessels2) %check how much the brain moved

%% Overlay Vessels and ISI images
%WIP
