# Variables containing source material and review questions for Study-Bot to use.

# NOTE: The information below was generated by Chat-GPT and GitHub Copilot and may not 
# be accurate or factually correct. This information is intended for testing and not 
# for educational use.

humanBody = """
Stomach: The stomach is an organ located in the upper abdomen that plays a vital role in 
the digestion of food. Its main function is to store and break down food into smaller 
particles through the process of mechanical and chemical digestion. The stomach secretes 
gastric juices, including hydrochloric acid and enzymes, which help in the breakdown of 
proteins. It also mixes the partially digested food with these juices to form a 
semi-liquid mixture called chyme, which is then gradually released into the small 
intestine for further digestion and absorption.

Liver: The liver is the largest internal organ in the human body and is located in the 
upper right abdomen. It performs numerous functions that are essential for maintaining 
overall health. One of its primary roles is the production and secretion of bile, a 
substance that aids in the digestion and absorption of fats. The liver also detoxifies 
harmful substances, metabolizes nutrients, stores vitamins and minerals, regulates 
blood glucose levels, produces blood-clotting proteins, and filters and removes old or 
damaged blood cells from circulation. Additionally, it plays a key role in the 
metabolism of drugs and toxins.

Colon: The colon, also known as the large intestine, is the final part of the digestive 
system. Its primary function is to absorb water, electrolytes, and some vitamins from 
the remaining indigestible food materials after the digestion and absorption of 
nutrients in the small intestine. The colon also houses a complex community of 
beneficial bacteria known as the gut microbiota, which helps in the fermentation of 
undigested carbohydrates and the production of certain vitamins, such as vitamin K and 
some B vitamins. It further assists in the formation and elimination of feces, 
contributing to the regulation of bowel movements.

Brain: The brain is the most complex organ in the human body and is responsible for
controlling all bodily functions. It is located in the head and consists of three main
parts: the cerebrum, cerebellum, and brainstem. The cerebrum is the largest part of the
brain and is divided into two hemispheres. It is responsible for higher functions such
as memory, language, and reasoning. The cerebellum is located at the back of the brain
and is responsible for coordinating voluntary movements and maintaining balance. The
brainstem connects the brain to the spinal cord and is responsible for controlling
involuntary functions such as breathing, heart rate, and blood pressure.

Kidney: The kidneys are two bean-shaped organs located in the upper abdomen. They play
an important role in maintaining homeostasis by regulating the composition and volume
of body fluids. The kidneys filter waste products from the blood and excrete them in
the form of urine. They also help in the regulation of blood pressure, the production
of red blood cells, and the activation of vitamin D.

Heart: The heart is a muscular organ located in the chest that pumps blood throughout
the body. It consists of four chambers: two atria and two ventricles. The atria receive
blood from the veins and pump it into the ventricles. The ventricles then pump the
blood out of the heart and into the arteries. The heart is responsible for supplying
oxygenated blood to the body and deoxygenated blood to the lungs for oxygenation.
"""

testQuestionsHumanBody = [
	"What is the main function of the stomach?",
	"Where is the liver located in the human body?",
	"What is the primary function of the colon?",
	"What are the three main parts of the brain?",
	"What is the role of the kidneys in the human body?",
	"What are the four chambers of the heart called?"
]

krebsCycle = """
The Krebs cycle, also known as the citric acid cycle or tricarboxylic acid cycle, is a 
vital metabolic pathway that takes place in the mitochondria of eukaryotic cells. It 
plays a central role in extracting energy from carbohydrates, fats, and proteins 
through the oxidative breakdown of acetyl-CoA. Here are the eight most important 
chemical compounds involved in the Krebs cycle, along with their roles:

Citrate (Citric Acid):
Citrate is the starting compound of the Krebs cycle. It forms when acetyl-CoA (from 
glucose, fats, or amino acids) combines with oxaloacetate, catalyzed by citrate synthase. 
Citrate is converted into its isomer, isocitrate, by aconitase. The production of citrate 
marks the initiation of the Krebs cycle.

Isocitrate:
Isocitrate is produced from citrate through the catalytic action of aconitase. Isocitrate 
is then transformed by isocitrate dehydrogenase into a-ketoglutarate, releasing a 
molecule of carbon dioxide and reducing NAD+ to NADH in the process.

a-Ketoglutarate:
a-Ketoglutarate is produced from isocitrate by isocitrate dehydrogenase. It undergoes 
oxidative decarboxylation by a-ketoglutarate dehydrogenase complex, releasing another 
molecule of carbon dioxide and reducing NAD+ to NADH. This step is critical in 
generating energy-rich molecules.

Succinyl-CoA:
a-Ketoglutarate is further processed into succinyl-CoA through the action of 
a-ketoglutarate dehydrogenase complex. This conversion releases a molecule of carbon 
dioxide and reduces NAD+ to NADH. The reaction also generates a high-energy thioester 
bond in succinyl-CoA.

Succinate:
Succinyl-CoA is converted to succinate through substrate-level phosphorylation. The 
energy from the high-energy thioester bond in succinyl-CoA is used to phosphorylate 
guanosine diphosphate (GDP), converting it into guanosine triphosphate (GTP).

Fumarate:
The conversion of succinate to fumarate is catalyzed by succinate dehydrogenase, 
which is embedded in the inner mitochondrial membrane and also functions as Complex II of 
the electron transport chain. This step directly reduces ubiquinone (CoQ) while 
converting succinate to fumarate.

Malate:
Fumarate is converted to malate through the action of fumarase. This reversible hydration 
reaction prepares the substrate for the next oxidative step.

Oxaloacetate:
The final step of the Krebs cycle involves the conversion of malate to oxaloacetate by 
malate dehydrogenase. This reaction also regenerates NAD+ from NADH. Oxaloacetate can 
then combine with a new acetyl-CoA molecule to initiate another round of the Krebs cycle.

In summary, the Krebs cycle serves as a pivotal pathway for energy production in cells. 
It involves a series of reactions that facilitate the oxidative breakdown of acetyl-CoA, 
leading to the generation of NADH and FADH2, which subsequently participate in the electron 
transport chain to produce ATP. Additionally, the cycle provides intermediates that are 
used in various biosynthetic pathways and play important roles in maintaining cellular 
metabolic balance.
"""

testQuestionsKrebsCycle = [
	"What is the starting compound of the Krebs cycle?",
	"What is the role of aconitase in the Krebs cycle?",
	"How is a-ketoglutarate produced in the Krebs cycle?",
	"What is the function of succinyl-CoA in the Krebs cycle?",
	"What is the role of succinate dehydrogenase in the Krebs cycle?",
	"What is the final product of the Krebs cycle?"
]