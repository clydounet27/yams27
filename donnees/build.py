# Transcription des feuilles de Yam's -> base de données
# Format par joueur : 1 2 3 4 5 6 brelan carre full ps gs yams chance
#   x = case barrée (0) ; Y = "100" écrit dans une case (yam's supplémentaire, case barrée)
import json, csv

RAW = """
PDF1 p1 haut-gauche|1 8 6 12 20 18 15 24 25 30 x x 16|1 6 9 12 20 18 15 16 25 30 40 x 21|2 4 6 16 15 18 18 x 25 30 x 50 23|210 248 207
PDF1 p1 haut-droite|1 6 9 12 10 18 12 x 25 30 x x 21|3 8 9 12 15 18 18 x x 30 40 x 22|1 2 x 16 15 18 12 4 25 30 x x 25|144 210 148
PDF1 p1 bas-gauche|4 6 12 16 20 18 15 20 25 30 x x 22|2 2 6 8 5 18 9 4 25 30 40 x 23|1 4 9 12 20 18 3 12 x 30 40 x 19|223 172 201
PDF1 p1 bas-droite|4 6 9 12 15 18 12 12 25 30 40 x 18|1 6 6 12 15 18 18 x 25 30 40 x 18|2 8 3 8 15 12 9 8 25 30 40 x 25|236 189 185
PDF1 p2 haut-gauche|1 2 9 16 15 18 15 x 25 30 40 50 22|4 6 12 16 15 24 9 4 25 30 40 x 20|2 4 9 8 20 18 9 x 25 30 40 x 19|243 240 184
PDF1 p2 haut-droite|4 4 9 16 5 18 12 x 25 30 40 50 17|2 6 9 12 20 18 18 x x 30 x x 26|1 4 9 8 20 18 18 x 25 30 40 x 27|230 176 200
PDF1 p2 bas-gauche|2 6 6 12 15 24 18 x 25 30 40 x 19|2 6 12 16 15 6 9 8 25 30 40 x 23|1 2 6 8 20 18 15 8 25 30 40 x 19|232 192 192
PDF1 p2 bas-droite|4 6 6 4 20 18 x x 25 30 40 50 21|3 8 12 16 15 18 18 x 25 30 40 50 23|4 6 x 8 10 18 18 x 25 30 40 x 19|224 293 178
PDF1 p3 haut-droite|2 8 9 12 10 18 12 12 25 30 40 x 19|4 6 6 12 15 24 9 20 x 30 40 x 18|1 4 Y 12 5 18 18 Y 25 30 40 50 18|197 219 421
PDF1 p3 bas-gauche|1 6 15 8 20 24 x 16 25 30 40 x 19|3 6 12 8 15 24 x x 25 30 x 50 18|1 4 9 8 15 x 15 x 25 30 40 x 13|239 226 160
PDF1 p4 haut-gauche|x 4 6 12 20 24 12 16 25 30 x x 16|2 6 6 12 25 18 6 x 25 30 40 x 22|2 6 12 16 15 18 15 x 25 30 40 x 21|200 227 235
PDF1 p4 haut-droite|3 4 6 8 20 18 15 x 25 30 x 50 21|1 4 9 16 20 18 15 x 25 30 40 x 26|2 4 6 8 20 24 18 20 25 30 40 x 21|200 229 253
PDF2 p1 haut-gauche|4 6 9 12 15 18 x 24 25 30 40 50 14|1 4 3 16 15 18 18 x 25 30 x x 21|2 4 12 16 15 18 12 x 25 30 x 50 17|282 151 236
PDF2 p1 haut-droite|4 8 12 8 15 24 18 x 25 30 x 50 17|1 4 9 16 15 18 18 x 25 30 40 50 19|x 4 6 16 15 12 18 x 25 30 40 x 23|246 280 189
PDF2 p1 bas-gauche|3 6 9 12 15 24 18 20 25 30 40 x 19|1 6 9 8 15 18 x 4 25 30 40 x 27|1 4 6 8 15 6 12 x 25 30 x x 22|256 183 129
PDF2 p1 bas-droite|2 4 9 16 20 18 15 16 25 30 x x 21|2 8 12 16 20 24 15 x 25 30 40 x 24|1 4 9 12 15 18 x x 25 30 x x 19|211 251 133
PDF2 p2 haut-gauche|1 6 3 16 10 24 18 16 25 30 40 x 23|1 6 6 12 25 18 15 20 25 30 40 x 20|2 6 6 8 10 12 12 x x 30 40 x 22|212 253 148
PDF2 p2 haut-droite|4 4 12 12 15 12 12 20 25 30 40 x 18|1 4 9 4 10 18 18 x x 30 40 50 14|4 4 9 12 15 18 12 x 25 30 40 x 19|204 198 188
PDF2 p2 bas-gauche|1 4 6 4 10 18 x 20 25 30 x x 17|2 8 9 12 15 24 6 24 25 30 40 x 23|2 2 9 12 20 6 x x 25 30 x x 21|135 253 127
PDF2 p2 bas-droite|4 6 12 4 20 18 15 x 25 30 40 50 23|2 6 9 12 15 18 15 24 25 30 40 x 19|1 6 6 16 15 24 6 x x 30 40 x 22|282 215 201
PDF2 p3 haut-gauche|2 6 9 12 10 24 18 Y Y 30 x 50 21|x 2 12 16 20 18 x 24 x 30 40 50 19|2 6 9 8 20 x 15 x 25 30 40 x 17|417 266 172
PDF2 p3 haut-droite|4 8 6 16 10 24 18 16 25 30 40 x 16|2 2 3 12 10 18 3 x x 30 40 x 27|1 2 12 12 20 24 18 24 25 30 40 x 19|248 147 262
PDF2 p3 bas-gauche|1 6 12 12 x 24 x x 25 30 40 x 18|x 6 6 16 20 18 18 x 25 30 40 x 21|3 2 6 12 15 18 15 24 25 30 x x 26|168 235 176
PDF2 p3 bas-droite|2 6 9 12 20 18 15 16 25 30 40 x 20|2 8 9 8 15 12 3 20 x 30 x 50 24|1 6 3 16 10 30 12 20 25 30 40 50 24|248 191 302
PDF2 p4 haut-gauche|4 6 6 12 15 18 15 20 25 30 40 x 18|1 4 9 12 15 24 15 12 25 30 40 50 22|1 6 6 12 10 18 Y x 25 30 40 50 18|199 294 316
PDF2 p4 haut-droite|1 4 9 16 20 6 12 24 25 30 40 x 22|1 8 6 8 20 18 x x 25 30 40 x 21|2 x 9 x 15 18 18 24 x 30 40 x 21|209 176 177
PDF2 p4 bas-gauche|1 6 6 12 15 24 18 x 25 30 40 x 24|1 6 12 16 20 12 15 16 25 30 40 x 22|1 4 9 16 5 18 9 16 25 30 x 50 21|236 250 204
PDF2 p4 bas-droite|1 6 12 12 15 18 18 x 25 30 x x 19|1 2 3 16 15 18 18 16 25 30 40 x 23|2 4 9 12 10 18 x x 25 30 40 50 24|191 207 224
PDF2 p5 haut-gauche|3 6 6 12 15 24 12 12 25 30 x x 13|1 4 6 8 20 24 18 24 25 30 x 50 24|1 4 9 4 15 24 15 x 25 30 40 x 21|193 269 188
PDF2 p5 haut-droite|1 2 9 16 15 18 12 x 25 30 40 50 15|3 4 6 16 15 24 x x 25 30 40 x 20|2 8 12 16 15 12 18 8 25 30 40 x 23|233 218 244
PDF2 p5 bas-gauche|3 2 9 16 20 24 18 x 25 30 40 x 24|1 6 6 16 20 24 15 24 25 30 40 x 25|4 8 6 12 15 18 9 x 25 30 40 x 25|246 268 227
PDF2 p5 bas-droite|3 6 12 12 20 18 18 12 25 30 40 x 18|2 6 6 16 15 18 15 24 25 30 x x 22|3 4 6 12 x 18 18 x x 30 40 x 22|249 214 153
PDF2 p6 haut-gauche|3 4 6 16 15 18 12 x 25 30 40 50 17|1 6 9 8 10 18 x 24 25 30 40 x 22|2 8 9 12 15 18 18 8 25 30 40 x 29|236 193 249
PDF2 p6 haut-droite|x 6 12 12 15 18 x 24 25 30 40 x 20|2 6 15 8 20 18 15 x 25 30 40 x 18|1 2 6 12 15 24 9 20 25 30 x 50 21|237 232 215
PDF2 p6 bas-gauche|1 6 6 8 20 18 18 16 25 30 x x 26|1 8 9 12 15 24 18 16 25 30 40 x 23|1 4 9 12 20 18 12 Y 25 30 40 50 26|174 256 382
PDF2 p6 bas-droite|4 6 3 16 15 18 15 24 25 30 x x 18|x 4 6 8 15 18 9 8 x 30 x x 18|2 4 6 12 15 24 9 x x 30 40 50 24|174 116 252
PDF2 p7 haut-gauche|1 6 9 12 15 12 12 4 25 30 40 x 13|1 6 3 16 15 24 18 x 25 30 40 x 26|1 4 6 12 15 18 15 x 25 30 40 50 23|170 239 259
PDF2 p7 haut-droite|1 8 9 12 20 18 15 20 25 30 x x 22|1 6 9 16 20 6 18 12 25 30 40 50 22|1 8 6 12 15 18 3 x 25 30 40 x 23|215 255 181
PDF2 p7 bas-gauche|3 8 9 8 20 24 15 16 25 30 40 x 22|3 6 6 12 15 12 15 x 25 30 40 x 27|1 4 6 16 20 6 15 x 25 30 40 50 22|255 191 235
PDF2 p7 bas-droite|2 4 6 16 15 18 18 20 25 30 x x 25|x 4 3 8 15 24 15 4 25 30 40 x 25|1 4 12 8 10 18 15 x 25 30 x x 19|179 193 142
PDF2 p8 haut-gauche|4 2 9 8 20 24 15 12 25 30 x x 22|2 4 9 4 15 18 15 x 25 30 x x 22|1 4 6 12 15 12 15 x 25 30 40 x 22|206 144 182
PDF2 p8 haut-droite|x 4 6 12 20 24 18 16 25 30 40 x 22|1 6 9 8 10 24 18 x 25 30 40 x 19|2 2 9 12 15 18 9 x 25 30 40 50 19|252 190 231
PDF2 p8 bas-gauche|4 2 6 12 10 24 12 16 25 30 40 x 14|1 6 6 12 10 18 9 8 25 30 40 x 22|2 6 9 12 10 18 18 x 25 30 x x 26|195 187 156
PDF2 p8 bas-droite|Y 4 6 16 10 18 15 x 25 30 40 50 22|x 6 9 12 20 18 x 16 25 30 40 50 22|1 2 12 16 15 18 12 x 25 30 40 x 24|330 283 230
PDF2 p9 haut-gauche|x 8 9 16 20 18 12 16 25 30 40 x 19|2 2 6 8 15 18 15 x 25 30 40 x 19|2 4 9 12 15 18 15 x 25 30 40 x 19|248 180 189
PDF2 p9 haut-droite|1 4 3 16 15 18 12 x 25 30 40 x 21|2 4 6 12 20 12 18 8 25 30 x x 22|2 2 9 12 15 24 15 Y 25 30 40 50 22|185 159 381
PDF2 p9 bas-gauche|1 6 9 16 15 24 18 x 25 30 40 x 26|1 6 9 12 15 18 6 8 25 30 x x 19|1 4 6 16 15 18 9 x 25 30 40 x 22|245 149 186
PDF2 p9 bas-droite|4 8 9 12 15 18 12 4 25 30 40 x 19|x 6 12 16 20 18 15 20 Y 30 x 50 23|3 2 9 16 15 24 15 x 25 30 40 x 27|231 345 241
PDF2 p10 haut-gauche|4 4 6 12 20 12 15 20 25 x 40 50 21|1 6 6 12 15 18 15 16 25 30 40 50 24|1 6 6 16 15 6 18 x 25 30 40 50 22|225 258 235
PDF2 p10 haut-droite|1 4 9 4 10 18 x 24 25 30 x x 12|2 6 6 16 15 18 15 x 25 30 40 x 19|2 4 9 8 20 18 12 x 25 30 40 50 21|137 227 239
PDF2 p10 bas-gauche|2 6 9 4 15 24 18 12 25 30 40 50 19|2 4 6 12 20 6 x Y 25 30 40 50 19|4 6 9 16 15 24 9 x 25 30 x x 18|254 314 191
PDF2 p10 bas-droite|4 4 9 4 10 12 x x 25 30 40 50 22|2 2 6 8 15 24 18 x 25 30 40 50 21|1 4 12 12 10 18 12 x 25 30 40 x 18|210 241 182
PDF2 p11 haut-gauche|4 8 12 16 15 18 12 24 25 30 40 50 20|2 4 6 8 15 18 18 8 25 30 40 x 21|3 2 9 16 15 18 6 x 25 30 40 x 17|309 195 216
PDF2 p11 haut-droite|1 2 6 12 10 18 18 x 25 30 40 x 19|x 4 12 16 10 18 18 x 25 30 40 x 20|1 2 6 12 x 18 18 x 25 30 40 x 19|181 193 171
PDF2 p11 bas-gauche|4 4 12 8 15 24 15 x 25 30 x x 21|1 6 12 12 15 24 18 x 25 30 x x 18|3 4 6 8 15 12 15 x 25 30 40 x 18|193 196 176
PDF2 p11 bas-droite|4 8 9 12 15 18 12 Y 25 30 40 50 23|2 8 6 12 5 24 3 24 25 30 40 x 19|1 2 6 16 10 18 18 x x 30 40 50 16|381 198 207
PDF2 p12 haut-gauche|2 4 12 12 15 18 x 20 25 30 40 50 17|2 6 9 12 20 18 12 x 25 30 40 50 19|2 6 9 12 15 24 9 20 x 30 40 50 21|280 278 273
PDF2 p12 haut-droite|x 2 9 16 15 18 x x 25 30 40 x 20|2 8 9 12 15 6 x x 25 30 40 x 21|4 8 6 8 15 18 15 16 25 30 40 x 20|175 168 205
PDF2 p12 bas-gauche|3 4 9 12 15 24 12 24 25 30 x x 22|4 6 9 16 10 12 9 12 25 30 40 x 22|4 6 9 12 15 18 9 x 25 30 40 x 22|215 195 225
PDF2 p12 bas-droite|x 4 x 8 20 18 15 24 x 30 40 50 18|2 6 6 8 10 18 6 x 25 30 40 x 25|3 6 9 16 20 24 12 x 25 30 40 x 23|227 176 243
PDF2 p13 haut-gauche|3 6 9 12 15 18 12 20 25 30 40 x 25|1 4 12 12 20 18 12 x 25 30 40 x 20|1 6 9 8 15 18 15 16 25 30 40 x 22|250 229 205
PDF2 p13 haut-droite|2 4 6 8 20 24 18 16 25 30 40 50 16|1 8 12 8 10 18 12 x 25 30 40 x 21|1 8 6 x 15 18 15 x 25 30 40 x 22|294 185 180
PDF2 p13 bas-gauche|1 6 12 4 15 18 15 20 x 30 40 x 25|2 4 12 12 15 24 15 x 25 30 40 x 29|2 6 12 x 15 18 18 x x 30 40 x 18|186 243 159
PDF2 p13 bas-droite|1 4 6 12 15 18 12 x 25 30 40 x 19|2 2 12 8 15 24 15 24 25 30 40 x 23|x 10 6 16 10 24 18 16 25 30 40 x 19|182 255 249
PDF2 p14 haut-gauche|3 4 6 12 15 18 18 20 25 30 40 50 19|x 6 9 12 20 18 15 x 25 30 40 x 20|2 8 12 12 15 18 x x 25 30 x x 19|260 230 176
PDF2 p14 haut-droite|4 6 12 12 15 18 15 16 25 30 40 50 21|x 8 9 12 20 18 18 8 25 30 x x 21|3 4 12 12 15 18 9 x 25 30 40 x 21|299 204 224
PDF2 p14 bas-gauche|x 2 6 16 5 18 15 12 25 x 40 x 26|1 4 9 12 15 24 15 20 25 30 40 50 25|1 6 9 12 20 18 x x 25 30 40 x 20|165 305 216
PDF2 p14 bas-droite|1 8 6 16 20 18 15 24 25 30 40 x 19|1 4 3 12 15 24 18 x 25 30 40 x 16|2 8 9 12 5 6 12 x 25 30 40 x 20|257 188 169
PDF2 p15 haut-gauche|1 6 9 8 20 18 Y 8 25 30 40 50 16|1 6 6 16 10 12 x 16 25 30 40 50 19|1 6 6 8 10 18 15 x 25 30 40 x 21|331 231 180
PDF2 p15 haut-droite|1 4 6 12 15 18 15 x 25 30 x x 24|x 8 9 12 20 18 15 x 25 30 40 x 21|2 4 9 8 15 18 6 x x 30 40 x 18|150 233 150
PDF2 p15 bas-gauche|1 6 6 12 15 24 3 x 25 30 40 x 18|2 6 6 8 10 24 18 x 25 30 40 x 18|3 4 3 12 15 24 12 16 25 30 40 x 19|215 187 203
PDF2 p15 bas-droite|3 4 9 12 15 18 18 x 25 30 40 x 26|3 2 6 12 15 24 18 20 25 30 40 x 19|x 8 9 12 15 24 15 8 25 30 40 50 23|200 214 294
PDF2 p16 haut-gauche|2 8 12 16 15 18 x 16 25 30 40 x 18|1 8 9 16 15 18 12 16 25 30 40 x 26|x 6 12 16 15 18 12 x 25 30 40 50 18|235 251 277
PDF2 p16 haut-droite|1 6 6 8 20 12 9 x 25 30 40 x 19|3 4 9 12 20 24 18 x 25 30 40 x 18|1 2 6 12 10 18 18 x 25 30 40 50 21|176 238 243
PDF2 p16 bas-gauche|2 6 9 12 20 x 15 20 25 30 40 x 16|x 4 9 12 15 24 x 8 25 30 40 50 20|2 2 6 12 15 24 15 8 25 30 40 x 18|195 247 197
PDF2 p16 bas-droite|3 4 9 12 15 24 9 x 25 30 40 x 16|x 8 9 12 15 24 12 16 25 30 40 50 27|1 6 9 12 10 6 12 x 25 30 40 x 23|222 303 174
PDF2 p17 haut-gauche|1 8 6 12 15 18 9 20 25 30 40 x 21|4 4 12 12 20 18 15 x 25 30 40 x 23|4 6 9 8 15 6 18 x 25 30 40 x 21|205 238 182
PDF2 p17 haut-droite|3 4 9 12 10 18 12 x 25 30 40 x 15|3 6 12 12 20 18 18 16 25 30 40 50 26|2 4 3 16 20 12 x 20 x 30 40 x 22|178 311 169
PDF2 p17 bas-gauche|4 4 9 16 15 18 12 8 x 30 40 x 23|2 6 9 8 15 18 18 20 25 30 40 x 21|2 8 9 16 15 6 12 x 25 30 40 x 17|214 212 180
PDF2 p17 bas-droite|1 2 6 12 15 18 18 16 25 30 x x 20|x 6 9 16 15 18 x 8 25 30 x 50 26|1 4 12 16 15 24 15 16 25 30 40 50 17|163 238 300
Photo 28/10 haut-gauche|1 6 6 12 15 24 15 x 25 30 40 x 20|4 4 9 8 15 24 18 24 25 30 40 x 25|1 8 9 12 20 24 18 12 25 30 40 x 25|229 261 259
Photo 28/10 haut-droite|2 4 6 16 10 18 15 16 25 30 x x 18|4 4 9 16 15 12 x x 25 30 40 x 21|3 x 12 12 10 18 x 24 x 30 40 50 23|160 176 242
Photo 28/10 bas-gauche|x 4 12 8 15 18 18 x 25 30 40 x 23|1 6 9 12 20 18 12 x 25 30 x 50 19|2 4 6 16 15 18 18 x 25 30 40 x 19|193 237 191
Photo 28/10 bas-droite|x 4 6 16 20 18 12 20 25 30 40 x 25|x 6 6 12 15 18 15 24 25 30 40 x 24|1 4 6 x 20 12 6 x 25 30 x 50 22|261 215 176
Photo 02/11 (1) haut-gauche|3 6 9 16 15 18 18 24 x 30 x 50 23|4 4 6 8 15 12 12 16 25 30 40 x 27|2 2 6 12 15 12 12 16 25 30 40 50 21|247 194 243
Photo 02/11 (1) haut-droite|1 8 12 12 15 12 12 x 25 30 40 x 9|1 6 6 4 20 18 18 4 x 30 x 50 23|3 8 9 12 15 18 x 12 25 30 40 50 23|176 180 280
Photo 02/11 (1) bas-gauche|1 4 6 12 10 18 15 x 25 30 40 x 20|x 6 6 12 15 12 x 16 25 30 x 50 21|1 6 9 8 15 6 18 x 25 30 40 x 17|181 193 175
Photo 02/11 (1) bas-droite|2 6 6 12 15 18 18 24 25 30 40 x 18|1 4 9 16 15 24 15 12 25 30 40 x 24|x 6 6 12 20 24 9 16 25 30 40 x 22|214 250 245
Photo 02/11 (2) haut-gauche|3 6 9 12 15 24 18 24 25 30 40 50 21|1 6 9 16 20 18 9 x 25 30 40 x 17|1 8 6 12 15 24 15 16 25 30 40 x 24|312 226 254
Photo 02/11 (2) haut-droite|2 4 6 12 15 24 15 8 x 30 40 x 14|1 6 3 12 20 12 18 x x x 40 x 17|4 8 9 12 10 24 x 20 x 30 40 50 23|205 129 265
Photo 02/11 (2) bas-gauche|4 6 9 8 15 18 15 x 25 30 40 50 17|1 4 12 16 10 24 12 20 25 30 40 x 28|2 8 6 16 15 18 15 x 25 30 40 x 18|237 257 228
Photo 02/11 (2) bas-droite|3 4 6 12 20 18 12 8 25 30 40 x 25|1 8 9 8 15 18 9 24 25 30 40 x 21|2 4 9 12 15 18 x 24 25 30 x x 20|228 209 159
"""

# Notes de lecture (valeurs déduites des totaux écrits)
NOTES = {
 "PDF1 p2 bas-gauche": "G, ligne 2 lue « 8 » mais total haut écrit 57 : retenu 6.",
 "PDF1 p3 bas-gauche": "G, petite suite raturée : comptée 30 (cohérent avec le total 226).",
 "PDF2 p1 bas-droite": "G, ligne 5 déduite à 20 d'après le sous-total 82.",
 "PDF2 p1 haut-gauche": "JM, grande suite raturée : comptée barrée (cohérent avec 236).",
 "PDF2 p4 haut-gauche": "JM, full et grande suite raturés : comptés 25 et 40 (cohérent avec 316).",
 "PDF2 p5 bas-droite": "JM, grande suite raturée : comptée 40 (cohérent avec 153).",
 "PDF2 p9 bas-droite": "JM, ligne 1 lue 4, sous-total écrit 69 : retenu 3.",
 "PDF2 p15 haut-gauche": "JM, ligne 6 retenue 18 d'après le sous-total 49.",
 "Photo 28/10 haut-droite": "JM : total lu 242, le calcul donne 222 (gagnant inchangé).",
 "Photo 28/10 bas-gauche": "JM, ligne 5 raturée lue 15 : sous-total écrit 59, recalculé 61.",
 "Photo 28/10 bas-droite": "JM, sous-total haut écrit 53, recalculé 43 (le total 176 est juste).",
 "Photo 02/11 (1) haut-gauche": "G : total lu 194, le calcul donne 199.",
 "Photo 02/11 (2) haut-gauche": "JM : total raturé (254 ?), le calcul donne 251.",
 "Photo 02/11 (2) haut-droite": "G, case des 3 réécrite : lue 3 (cohérent avec le sous-total 54).",
 "Photo 02/11 (2) bas-droite": "R : total écrit 228, recalculé 238. G : sous-total écrit 60, les cases donnent 59 (total 208 au lieu de 209).",
 "PDF2 p8 haut-gauche": "R, ligne 4 illisible : retenu 8 d'après le sous-total 67.",
 "PDF2 p13 bas-gauche": "JM, ligne 4 comptée barrée d'après le sous-total 53.",
 "PDF2 p7 haut-gauche": "R, yam's raturé compté barré. JM : total écrit 259 mais le calcul donne 239 → égalité avec G (confirmé).",
 "PDF2 p16 haut-droite": "JM : total écrit 243 mais le calcul donne 233 → c'est G (238) qui gagne (confirmé).",
}
# La feuille PDF1 p3 haut-gauche (Léa, Gabr, GM, GP) est barrée et concerne d'autres joueurs : exclue.

CATS = ["1","2","3","4","5","6","Brelan","Carré","Full","PS","GS","Yam's","Chance"]
PLAYERS = ["R","G","JM"]
VALID = {0:[i*1 for i in range(6)],1:[i*2 for i in range(6)],2:[i*3 for i in range(6)],3:[i*4 for i in range(6)],
         4:[i*5 for i in range(6)],5:[i*6 for i in range(6)],6:[0,3,6,9,12,15,18],7:[0,4,8,12,16,20,24],
         8:[0,25],9:[0,30],10:[0,40],11:[0,50],12:list(range(0,31))}

def score(tokens):
    cells, extra = [], 0
    for i,t in enumerate(tokens):
        if t == "x": cells.append(None)
        elif t == "Y": cells.append("Y"); extra += 1
        else:
            v = int(t); assert v in VALID[i], (i, v); cells.append(v)
    num = lambda c: c if isinstance(c,int) else 0
    upper = sum(num(c) for c in cells[:6])
    bonus = 35 if upper >= 63 else 0
    yams_n = (1 if cells[11] == 50 else 0) + extra
    yams_pts = (50 if cells[11] == 50 else 0) + 100*extra
    lower = sum(num(c) for c in cells[6:11]) + num(cells[12])
    return dict(cells=cells, upper=upper, bonus=bonus, yams=yams_n, yamsPts=yams_pts,
                lower=lower, total=upper+bonus+lower+yams_pts)

games, anomalies = [], []
for n, line in enumerate([l for l in RAW.strip().splitlines() if l.strip()], 1):
    src, *cols, written = line.split("|")
    written = list(map(int, written.split()))
    g = {"id": n, "source": src, "players": {}, "note": NOTES.get(src)}
    for p, col, w in zip(PLAYERS, cols, written):
        t = col.split(); assert len(t) == 13, (src, p)
        s = score(t); s["written"] = w
        g["players"][p] = s
        if s["total"] != w:
            anomalies.append(f"#{n} {src} {p}: écrit {w}, calculé {s['total']}")
    best = max(s["total"] for s in g["players"].values())
    g["winners"] = [p for p,s in g["players"].items() if s["total"] == best]
    games.append(g)

# ---- Parties du tableur (onglets Stats et Stats_2), placées avant les feuilles papier
ODS_NOTES = {
 ("Stats",12,"R"): "R : case des 3 saisie à 1 dans le tableur (valeur impossible), conservée.",
 ("Stats",153,"JM"): "JM : case des 4 saisie à 6 dans le tableur (valeur impossible), conservée.",
 ("Stats",191,"R"): "R : case des 4 saisie à 9 dans le tableur (valeur impossible), conservée.",
 ("Stats_2",61,"G"): "G : carré saisi à 1 dans le tableur (valeur impossible), conservé.",
 ("Stats_2",100,"G"): "G : case des 5 saisie à 30 dans le tableur (valeur impossible), conservée.",
 ("Stats_2",169,"G"): "G : carré saisi à 25 dans le tableur (valeur impossible), conservé.",
 ("Stats",53,None): "Total de G saisi 224, recalculé 213 → c'est JM (218) qui gagne.",
}
LABEL = {"Stats":"Tableur Stats","Stats_2":"Tableur Stats 2"}
ods = json.load(open("ods_raw.json"))
ods_games = []
for o in ods:
    g = {"source": f"{LABEL[o['sheet']]} n°{o['n']}", "series": LABEL[o['sheet']], "players": {}, "note": None}
    notes = []
    for p_raw, r in o["rows"].items():
        p = p_raw.upper(); r = [int(a) for a in r]
        up = sum(r[:6]); bonus = 35 if up >= 63 else 0
        yp = r[13]; yn = 0 if yp == 0 else 1 + (yp - 50)//100
        cells = [v if v else None for v in r[:6]] + [v if v else None for v in r[8:13]]
        cells.insert(11, 50 if yn else None); cells = cells[:12] + [r[14] if r[14] else None]
        lower = sum(r[8:13]) + r[14]
        g["players"][p] = dict(cells=cells, upper=up, bonus=bonus, yams=yn, yamsPts=yp, lower=lower,
                               total=up+bonus+lower+yp, written=r[15])
        if (o['sheet'],o['n'],p) in ODS_NOTES: notes.append(ODS_NOTES[(o['sheet'],o['n'],p)])
    if (o['sheet'],o['n'],None) in ODS_NOTES: notes.append(ODS_NOTES[(o['sheet'],o['n'],None)])
    g["note"] = " ".join(notes) or None
    best = max(s["total"] for s in g["players"].values())
    g["winners"] = [p for p in PLAYERS if g["players"][p]["total"] == best]
    g["players"] = {p: g["players"][p] for p in PLAYERS}
    ods_games.append(g)
for g in games:
    g["series"] = "Photo" if g["source"].startswith("Photo") else "Feuilles PDF"
games = ods_games + games
for i, g in enumerate(games, 1): g["id"] = i

json.dump({"categories": CATS, "players": PLAYERS, "series": ["Tableur Stats","Tableur Stats 2","Feuilles PDF","Photo"], "games": games}, open("yams_data.json","w"), ensure_ascii=False)
with open("yams_parties.csv","w",newline="",encoding="utf-8-sig") as f:
    w = csv.writer(f, delimiter=";")
    w.writerow(["partie","source","joueur"]+CATS[:6]+["Total haut","Bonus"]+CATS[6:11]+["Yam's (pts)","Nb yam's","Chance","Total","Total écrit","Gagnant"])
    for g in games:
        for p,s in g["players"].items():
            c = s["cells"]; fmt = lambda v: "X" if v is None else ("100→Yam's" if v=="Y" else v)
            w.writerow([g["id"],g["source"],p]+[fmt(v) for v in c[:6]]+[s["upper"],s["bonus"]]+[fmt(v) for v in c[6:11]]
                       +[s["yamsPts"],s["yams"],fmt(c[12]),s["total"],s["written"],"oui" if p in g["winners"] else ""])
print(len(games), "parties", sum(len(g["winners"])>1 for g in games), "égalités"); print("\n".join(anomalies))
