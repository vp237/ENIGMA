filename = 'Short.mp3';
[Y, Fs] = audioread(filename);
T = 1/Fs;
L = 16500;
t = (0:L-1)*T;
P2 = abs(Y/L);
P1 = P2(1:L/2+1);
P1(2:end-1) = 2*P1(2:end-1);
f = Fs*(0:(L/2))/L;
plot(f,P1) 
title('Single-Sided Amplitude Spectrum of X(t)')
xlabel('f (Hz)')
ylabel('|P1(f)|')

time = 1:16500;
syn = 10000*sin(2*pi*8924*time) + 10000*sin(2*pi*15000*time) + 10000*sin(2*pi*15580*time) + 10000*sin(2*pi*14230*time)+ 10000*sin(2*pi*21950*time);
sound(syn, Fs);
