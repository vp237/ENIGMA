filename = 'Typewriter.mp3';
[y, Fs] = audioread(filename);
r = range(y);
mi = min(y);
ma = max(y);
sound(y, Fs);

y_new_1 = round((y(:,1)-mi(1)).*4095./r(1));
y_new_2 = round((y(:,2)-mi(2)).*4095./r(2));
y_new   = [y_new_1, y_new_2];
% y_new     = round((y-mi).*4095./r);


% y_trunc = transpose(y_new(1:16700));
% man = max(y_trunc);
% minn = min(y_trunc);
csvwrite('Channel_A.csv', transpose(y_new(:,1)));
csvwrite('Channel_B.csv', transpose(y_new(:,2)));
% csvwrite('Channel_A.csv', transpose(y_new));