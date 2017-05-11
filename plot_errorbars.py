import numpy as np
import matplotlib.pyplot as plt
#from matplotlib.ticker import NullFormatter

#x = range(21)[1:]


'''
y0 = [1.96788,1.95736,2.72092,5.5974,6.47844,5.1152,8.75292,11.49792,10.98436,12.35424,13.3708,12.97392,15.09724,13.57916,15.14624,16.15368,19.84572,22.71456,19.6526,24.10236]
yerror0 = [0.0562055655607,0.0272673871135,0.822265257444,2.90354251217,5.2303074562,2.73788835419,7.28460503758,7.58345173609,8.7448607988,9.66813398865,8.34191313788,9.84905945934,10.9043541405,9.19856552591,10.0085273573,12.2972391234,13.4925091114,13.3637466605,13.7782192928,13.482630197]

y1 = [0.5,0.5,0.5333334,0.60588196,0.60901532,0.58002992,0.6329596,0.68798444,0.65065216,0.65905,0.6972344,0.6615264,0.6905514,0.68766648,0.69038252,0.68790612,0.70186916,0.73998636,0.71025336,0.73307636]
yerror1 = [0.0,0.0,0.0666668,0.118739290004,0.124112125593,0.103571461074,0.128530338048,0.113036742919,0.135033478841,0.133432547182,0.116463316825,0.144426743815,0.122498662352,0.122835044045,0.12201357872,0.124930032157,0.148634886731,0.123615481818,0.134599936826,0.119437810687]

y2 = [0.880866,0.880866,0.8881514,0.90797756,0.90861024,0.90037928,0.9151204,0.92879768,0.92056632,0.922404,0.93264564,0.92362904,0.93048372,0.92992544,0.930549,0.9292334,0.9354278,0.94509632,0.93663972,0.94347604]
yerror2 = [0.0,0.0,0.0145708,0.0326585579364,0.033821262483,0.0269300499985,0.0350887589578,0.0318979665493,0.0377381981242,0.0373097105537,0.0337024189184,0.0400835917367,0.0340690802876,0.0350919108754,0.0340260930734,0.0349483573531,0.041414189012,0.0353399919748,0.0377493735085,0.0343445215701]
'''

# Times for tushar, -e, -rw, -w, -s CORA

t0 = [np.mean([39.933, 48.221, 48.884, 50.814, 50.338, 49.096, 50.683, 50.815, 47.633, 47.338, 45.193, 50.6, 51.98, 47.453, 47.125, 51.656, 54.015, 50.934, 54.178, 53.866, 52.885, 50.355, 53.394, 50.886, 48.692])] * 9
t1 = [np.mean([47.975, 50.827, 51.168, 45.34, 47.142, 49.645, 48.312, 46.616, 46.68, 48.227, 49.636, 45.067, 49.173, 49.5, 47.995, 48.124, 45.787, 45.844, 46.857, 46.596, 44.829, 45.629, 45.919, 49.922, 46.477])] * 9
t2 = [2.0081600000000002, 1.9583599999999999, 4.6955199999999992, 3.5706399999999996, 2.9937999999999994, 3.7145199999999998, 4.2310400000000001, 3.6066000000000003, 4.3780399999999995]
t3 = [1.9617600000000002, 34.977400000000003, 39.839480000000002, 38.973080000000003, 38.423319999999997, 39.992360000000005, 39.489920000000005, 39.554040000000001, 39.361399999999996]
t4 = [2.1315600000000003, 3.6211999999999995, 7.2659600000000015, 7.5377199999999993, 18.152200000000001, 32.690359999999998, 31.97212, 32.672280000000001, 32.672240000000002]

t0error = [0] * 9
t1error = [0] * 9
t2error = [0.1638195788054651, 0.053004060221835819, 0.46441508330371878, 1.7206804207638327, 0.80269316678292457, 1.6333033060641249, 2.422435608721107, 1.8267522875310707, 1.8872882870404297]
t3error = [0.049397392643741857, 1.3128565191977377, 1.8029651160241578, 1.4168067735580605, 2.106691220278853, 1.3702784207598109, 2.2337486325905158, 1.7136092782195131, 1.4578251198274779]
t4error = [0.21544708491878004, 0.10501199931436409, 0.207033230182983, 0.20929109297817722, 1.2494403547188637, 1.5625406459993287, 1.5142659296173839, 2.3116854893345673, 1.9405723543326081]


# AUC ROC CORA

t0 = [np.mean([0.846094, 0.850037, 0.846684, 0.846343, 0.850099, 0.845722, 0.845101, 0.845753, 0.850876, 0.842368, 0.842524, 0.848578, 0.845877, 0.84805, 0.848454, 0.849478, 0.841903, 0.849106, 0.846995, 0.849696, 0.847988, 0.846808, 0.85072, 0.846156, 0.846467])] * 9
t1 = [np.mean([0.840878, 0.846467, 0.847274, 0.84389, 0.846808, 0.848951, 0.849168, 0.842337, 0.841747, 0.845722, 0.841654, 0.849447, 0.849323, 0.844262, 0.850845, 0.841841, 0.849727, 0.842368, 0.848516, 0.846436, 0.846715, 0.849944, 0.845939, 0.848268, 0.845101])] * 9
t2 = [0.5, 0.5, 0.5, 0.51333336000000007, 0.56666680000000003, 0.57268759999999996, 0.58520627999999997, 0.59935432000000011, 0.59634392000000003]
t3 = [0.5, 0.84611528000000003, 0.84546336, 0.84624571999999998, 0.84586067999999992, 0.84728267999999995, 0.84592520000000004, 0.84595627999999989, 0.84612148000000009]
t4 = [0.5, 0.5, 0.66666700000000001, 0.66666700000000001, 0.75413303999999992, 0.84600360000000008, 0.84597628000000002, 0.84637240000000002, 0.84578003999999996]

t0error = [0] * 9
t1error = [0] * 9
t2error = [0.0, 0.0, 0.0, 0.045215623651901564, 0.081649821392088803, 0.091036976647074566, 0.11075671468674755, 0.090246327517398736, 0.086622735090007411]
t3error = [0.0, 0.0019976114040523439, 0.0027734287354103768, 0.0027716367658118723, 0.0026247134353296485, 0.0025216055634456397, 0.0025317603520080699, 0.0030265661535145752, 0.002273825589089902]
t4error = [0.0, 0.0, 0.0, 0.0, 0.0024336014049963148, 0.0027027699717141942, 0.0021783422048888327, 0.002131525669561601, 0.0027605765844113052]

# AUC PR CORA

t0 = [np.mean([0.975251, 0.97591, 0.975539, 0.975419, 0.976069, 0.975221, 0.975018, 0.975227, 0.976033, 0.974675, 0.97473, 0.975649, 0.975278, 0.975439, 0.975637, 0.975872, 0.974533, 0.975781, 0.975322, 0.975991, 0.975532, 0.975479, 0.976061, 0.975251, 0.975359])] * 9
t1 = [np.mean([0.974192, 0.975458, 0.975506, 0.974907, 0.975479, 0.975861, 0.975997, 0.974672, 0.974477, 0.975221, 0.974442, 0.975903, 0.975816, 0.974882, 0.975999, 0.974511, 0.975957, 0.974675, 0.975635, 0.975452, 0.975447, 0.976014, 0.975196, 0.975698, 0.975019])] * 9
t2 = [0.88086600000000004, 0.88086600000000004, 0.88086600000000004, 0.88378016000000015, 0.89543680000000014, 0.89762048000000005, 0.90230460000000012, 0.90344880000000005, 0.9023569600000001]
t3 = [0.88086600000000004, 0.97529100000000002, 0.97520272000000008, 0.97532436, 0.97528856000000008, 0.97551704000000017, 0.97527823999999996, 0.97528432000000009, 0.97531428000000009]
t4 = [0.88086600000000004, 0.88086600000000004, 0.91729300000000014, 0.91729300000000014, 0.94984047999999999, 0.97528411999999998, 0.97531072000000008, 0.97533844000000003, 0.9752450399999999]

t0error = [0] * 9
t1error = [0] * 9
t2error = [0.0, 0.0, 0.0, 0.009882397371812162, 0.01784551257207256, 0.021650715543131586, 0.02965334399625107, 0.021255386150338451, 0.019762721435025079]
t3error = [0.0, 0.00033883931294937698, 0.00052654781511274394, 0.00050867065022468683, 0.0004810417096261014, 0.00044668856981122293, 0.00046429553346980591, 0.00056585056119084749, 0.00039375693212945933]
t4error = [0.0, 0.0, 1.1102230246251565e-16, 1.1102230246251565e-16, 0.0011039112688980088, 0.00047208256227062711, 0.00036014036374725362, 0.00039724733655495544, 0.00049092479912915717]

# Training Time: WebKB

#t0 = [np.mean([4.056, 4.036, 3.676, 3.84, 3.971, 4.001, 4.847, 3.761, 3.973, 5.558, 3.984, 4.188, 3.582, 3.745, 3.642, 4.796, 3.482, 3.788, 3.995, 3.999, 3.467, 3.763, 3.696, 3.705, 3.966])] * 5
#t1 = [np.mean([4.619, 3.986, 3.613, 4.318, 5.101, 3.974, 4.27, 3.969, 4.135, 4.147, 3.907, 3.964, 3.936, 3.976, 4.835, 3.988, 3.796, 3.83, 3.978, 4.072, 4.292, 3.982, 3.744, 4.229, 4.184])] * 5
t0 = [np.mean([[4.056, 4.036, 3.676, 3.84, 3.971, 4.001, 4.847, 3.761, 3.973, 5.558, 3.984, 4.188, 3.582, 3.745, 3.642, 4.796, 3.482, 3.788, 3.995, 3.999, 3.467, 3.763, 3.696, 3.705, 3.966][5:10]])] * 5
t1 = [np.mean([4.619, 3.986, 3.613, 4.318, 5.101, 3.974, 4.27, 3.969, 4.135, 4.147, 3.907, 3.964, 3.936, 3.976, 4.835, 3.988, 3.796, 3.83, 3.978, 4.072, 4.292, 3.982, 3.744, 4.229, 4.184][6:11])] * 5
t2 = [4.6683999999999992, 4.4949599999999998, 4.3741999999999992, 4.4880400000000007, 4.5865600000000004]
t3 = [4.5006400000000006, 4.5491200000000003, 4.827160000000001, 4.6657600000000006, 4.74552]
t4 = [4.6815600000000002, 4.6512399999999996, 4.7423999999999999, 4.8572800000000003, 4.7600800000000003]

t0error = [0] * 5
t1error = [0] * 5
t2error = [0.84866422099673788, 0.55425030302201916, 0.87277103526640931, 0.65503150947110933, 0.60591293632006238]
t3error = [0.73040935809996299, 1.0681218402410839, 0.859344200189889, 0.83165244086697654, 0.70228228626386402]
t4error = [0.4924815594517219, 0.59285325536763323, 0.72300970947837206, 0.79276329481125696, 0.62486317990420914]

#x = range(10)[1:]
x = range(6)[1:]
fig = plt.figure()
axes = plt.gca()
#axes.set_ylim([0, 52])
axes.set_ylim([3,6])

plt.errorbar(x, t0, yerr=t0error, fmt='k--') # Tushar
plt.errorbar(x, t1, yerr=t1error, fmt='c--') # -e
plt.errorbar(x, t2, yerr=t2error, fmt='r-o') # -rw
plt.errorbar(x, t3, yerr=t3error, fmt='b-o') # -w
plt.errorbar(x, t4, yerr=t4error, fmt='g-o') # -s

plt.title('WebKB: Training Time vs. Number of Predicates')
plt.xlabel('Number of predicates')
plt.ylabel('Time (seconds)')


plt.show()

# ax0: Time

'''

ax0.errorbar(x, t0, yerr=t0error, fmt='-o')
ax0.set_xlabel('Number of Features')
ax0.set_ylabel('AUC ROC')
ax0.set_title('Tushar')

ax0.set_xlim([0, 10])
#ax0.set_ylim([0, max([max(t0), max(t1)]) + max([max(t0error), max(t1error)]) + 1])
ax0.set_ylim([0.4, 1.0])

# ax1: AUC ROC
ax1.errorbar(x, t1, yerr=t1error, fmt='-o')

ax1.set_xlabel('Number of Features')
ax1.set_ylabel('AUC ROC')
ax1.set_title('-e')

ax1.set_xlim([0, 10])
#ax1.set_ylim([0, max([max(t0), max(t1)]) + max([max(t0error), max(t1error)]) + 1])
ax1.set_ylim([0.4, 1.0])

'''

#fig, (ax2, ax3, ax4) = plt.subplots(ncols=3, figsize=(15,5))
#fig, (ax2, ax3, ax4) = plt.subplots(ncols=1, figsize=(5,5))
#, sharex=True)
#fig = plt.subplots(t, t, 'r--', t, t**2, 'bs', t, t**3, 'g^', figsize=(5,5))
#fig = plt.plot(t, t, 'r-o', t, t**2, 'b-o', t, t**3, 'g-o', linewidth=2.0)

#fig.suptitle('Cora: 10 Trees, 25 Independent Runs. AUC ROC:')


'''
# ax2: AUC PR

ax2.errorbar(x, t2, yerr=t2error, fmt='-o')

ax2.set_xlabel('Number of Predicates')
ax2.set_ylabel('Time (seconds)')
ax2.set_title('Random Paths')

ax2.set_xlim([1, 9])
ax2.set_ylim([0, max(t2 + t3 + t4) + max(t2error + t3error + t4error) + 1])
#ax2.set_ylim([0.4, 1.0])

# ax3: AUC PR

ax3.errorbar(x, t3, yerr=t3error, fmt='-o')

ax3.set_xlabel('Number of Predicates')
ax3.set_ylabel('Time (seconds)')
ax3.set_title('Walked Paths')

ax3.set_xlim([1, 9])
ax3.set_ylim([0, max(t2 + t3 + t4) + max(t2error + t3error + t4error) + 1])
#ax3.set_ylim([0.4, 1.0])

# ax4


ax4.errorbar(x, t4, yerr=t4error, fmt='-o')

ax4.set_xlabel('Number of Predicates')
ax4.set_ylabel('Time (seconds)')
ax4.set_title('Shortest Paths')

ax4.set_xlim([1, 9])
ax4.set_ylim([0, max(t2 + t3 + t4) + max(t2error + t3error + t4error) + 1])
#ax4.set_ylim([0.4, 1.0])

#fig.set_size_inches(15, 5)
#plt.figure(figsize=(3,1))
#plt.savefig('THIS_IS_TESTING.png', dpi=600)
'''


