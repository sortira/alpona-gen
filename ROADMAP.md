# Alpona-Gen Project Roadmap
**Last Updated:** October 10, 2025

## Stage 1: Foundation & Baseline (Immediate Next Steps)
**Focus:** Solidifying the current codebase, expanding artistic variety, and establishing a benchmark for AI generation.

#### 🎯 Task 1.1: Integrate New Patterns & Refactor Configuration
**Goal:** Increase the generator's creative range and make it easier for anyone to experiment with.

**Action Items:**
- [ ] Integrate the 10 new pattern functions (sunburst, lotus_petals, gear_teeth, etc.) into `patterns.py`.
- [ ] Update the `filled_styles` and `outlined_styles` lists in `fractalpona.py` to include the new patterns.
- [ ] Create a `config.yaml` file to manage parameters like image size, layer counts, and color palettes.
- [ ] Modify `fractalpona.py` to load these settings from the `config.yaml` file instead of using hardcoded values.

#### 🤖 Task 1.2: Train a Baseline Generative Model (GAN)
**Goal:** Achieve the project's original aim of AI generation and establish a performance benchmark to compare future models against.

**Action Items:**
- [ ] Set up a Python environment for machine learning (PyTorch or TensorFlow).
- [ ] Choose and implement a simple, well-understood GAN architecture (e.g., DCGAN).
- [ ] Train the model on the existing 13,000 image dataset.
- [ ] Document the results, saving the model checkpoint and a sample of the best-generated images.

#### 📚 Task 1.3: Enhance Project Documentation
**Goal:** Make the project more welcoming, accessible, and understandable for collaborators and users.

**Action Items:**
- [ ] Create a `CONTRIBUTING.md` file in the GitHub repository, explaining how others can add their own pattern functions.
- [ ] Add a `GALLERY.md` or a "Showcase" section to the main README to display the most beautiful generated images.
- [ ] Update the `README.md` to reflect all the new patterns and the new configuration system.

---

## Stage 2: Artistic Evolution & AI Advancement (Mid-Term Goals)
**Focus:** Adding significant new artistic capabilities to the generator and training state-of-the-art AI models.

#### 🏷️ Task 2.1: Create a Labeled Dataset (v2.0)
**Goal:** Transform the dataset from a collection of images into structured, machine-readable data. This is the key prerequisite for advanced AI.

**Action Items:**
- [ ] Modify `fractalpona.py` to track the sequence of patterns used for each generation.
- [ ] For each generated image (`image_xyz.png`), save a corresponding metadata file (`image_xyz.json`) containing the list of styles used.
- [ ] Re-generate the full dataset with this new labeling system and upload it as a new version to Kaggle.

#### 🎨 Task 2.2: Evolve the Generator's Artistic Capabilities
**Goal:** Move beyond purely radial patterns to increase the authenticity and complexity of the art.

**Action Items:**
- [ ] **Introduce Motifs:** Research and implement non-circular motifs common in Alpona, such as the Paisley (কলকা), fish, or flower shapes, and create patterns to place them symmetrically.
- [ ] **Generate Animations:** Add a feature to save frames after each layer is drawn and stitch them into a video, showing the mesmerizing process of creation.
- [ ] **Add Textures & Imperfections:** Implement options for subtle background textures and minor "wobbles" in the lines to give the art a more organic, hand-drawn feel.

#### 🧠 Task 2.3: Train State-of-the-Art AI Models
**Goal:** Leverage the new dataset to create high-quality, controllable generative models.

**Action Items:**
- [ ] **Fine-tune a Diffusion Model:** Use the labeled dataset to fine-tune a pre-trained model like Stable Diffusion. This will likely produce the highest quality and most novel Alpona images.
- [ ] **Train a Conditional GAN:** Use the style labels from the v2.0 dataset to train a cGAN, which would allow for generating images with specific requests (e.g., "generate an Alpona with a `draw_lotus_petals` layer").

---

## Stage 3: Community & Platform (Long-Term Vision)
**Focus:** Transforming Alpona-Gen from a project into an interactive tool and a platform for creativity.

#### 🌐 Task 3.1: Develop an Interactive Web UI
**Goal:** Make Alpona-Gen accessible to everyone, especially non-programmers and artists.

**Action Items:**
- [ ] Build a web application using a framework like Streamlit or Gradio.
- [ ] Create a user interface where users can select patterns for each layer from a dropdown menu.
- [ ] Add sliders and color pickers for users to customize their generation in real-time.
- [ ] Include a button to download the final high-resolution artwork.

#### ✒️ Task 3.2: Bridge Digital and Physical Art
**Goal:** Bring the procedurally generated art out of the screen and into the physical world.

**Action Items:**
- [ ] Add an option to the generator to export designs as SVG (Scalable Vector Graphics) files.
- [ ] Use the SVG output to create physical drawings with a pen plotter, exploring different types of paper and inks.

#### 🎓 Task 3.3: Academic & Cultural Contribution
**Goal:** Solidify the project's contribution to the fields of computational creativity and digital humanities.

**Action Items:**
- [ ] **Write a Paper/Article:** Author a research paper or a detailed article about the process of algorithmically modeling a traditional folk art form. Submit to a relevant conference (e.g., SIGGRAPH) or journal.
- [ ] **Host a Workshop:** Collaborate with a local university or cultural center in Kolkata to host a "Creative Coding with Alpona-Gen" workshop, teaching others how to blend art and technology.