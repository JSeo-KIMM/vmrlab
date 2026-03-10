# Peer Review: Mixed Reality Navigation System for Ultrasound-Guided and Fusion Biopsies Using Markerless Instrument Tracking

**Reviewer:** Paper Reviewer Pro (Robotics & Kinematics Expert)
**Date:** 2026-03-10
**File:** manuscript.pdf

---

## Summary and Opening

This paper presents a mixed reality navigation system for ultrasound-guided and fusion biopsies that integrates markerless tracking of both a biopsy needle and an ultrasound probe using a Microsoft HoloLens 2 headset. The system combines real-time US image overlay with pre-procedural 3D CT/MRI data, enabling the operator to visualize anatomical context without fiducial markers. The key strengths of this work include the comprehensive system integration (needle tracking, probe tracking, and multi-modal fusion in a single markerless pipeline), the thorough ablation study on pose estimation methods, and the practical biopsy navigation assessment demonstrating a significant improvement in target hit rate (87.14% vs. 32.86%).

However, the following concerns must be addressed before this manuscript can be considered for acceptance.

---

## Review Comments

**Comment 1:** Lack of statistical rigor in the biopsy navigation assessment

The biopsy navigation assessment (Section: Biopsy Navigation Assessment, page 7) was performed by only a single operator "without prior experience in performing medical procedures." This severely limits the generalizability of the results. The 87.14% vs. 32.86% comparison lacks statistical significance testing (e.g., paired t-test, Wilcoxon signed-rank test). The authors should recruit multiple operators with varying levels of experience and report inter-operator variability with appropriate statistical tests.

**Comment 2:** Insufficient description of the CT-US registration methodology

The multi-modal image fusion method (Section: Multi-modal image fusion, page 4) is described at a very high level. The authors state that "the estimated position and orientation of the US image determines the cutting plane through the superimposed volumetric data," but the precise mathematical formulation of how the 2D US plane is extracted from the 3D CT/MRI volume is not provided. Given that this is a core contribution, a formal description with coordinate transformations and equations is necessary.

**Comment 3:** Potential conflict of interest insufficiently addressed

The competing interests section (page 13) states that the authors are MedApp S.A. employees and that MedApp S.A. produces the CarnaLife Holo solution used in the study. While disclosed, this represents a significant conflict of interest. The evaluation relies heavily on the proprietary CarnaLife Holo platform (Ref. 25), making independent reproducibility difficult. The authors should discuss how this potential bias was mitigated and consider providing access to at least the markerless tracking components for independent verification.

**Comment 4:** Limited validation environment — rigid phantom only

The CT-US target registration error (Section: CT-US Target Fusion Error, page 7) was evaluated only on a rigid radiological phantom. The authors acknowledge this limitation but do not sufficiently address its implications. In real clinical scenarios, tissue deformation due to breathing, probe pressure, and patient movement would significantly affect registration accuracy. The claimed TRE of 1.97 ± 0.89 mm is likely optimistic. The authors should at least discuss expected degradation under deformable conditions or provide preliminary results on a deformable phantom.

**Comment 5:** Biopsy navigation test does not incorporate CT/MRI fusion

The biopsy navigation assessment (page 7) explicitly states: "The test did not incorporate fusion of US with CT/MRI but evaluated in practice suitability of both needle and US probe tracking accuracy." This is a significant gap because the paper's title and abstract emphasize "Fusion Biopsies." The practical benefit of the complete system (including fusion) remains unvalidated. The authors should either include a fusion-based navigation experiment or clearly qualify the scope of validation in the title and abstract.

**Comment 6:** Equation notation inconsistencies and insufficient explanation

In Equations (1) and (2) on page 4, the symbols $\hat{P}$, $\bar{P}$, $\mathscr{S}_M$, and $\mathscr{V}_M$ are introduced but their definitions appear only after the equations. The notation $\mathscr{S}_M$ (set of object symmetries) and $\mathscr{V}_M$ (set of points sampled from the 3D model) should be defined before or alongside the equations. Additionally, the relationship between MSSD/MSPD metrics and the actual clinical relevance (e.g., what MSSD threshold corresponds to acceptable clinical accuracy) is not discussed.

**Comment 7:** Runtime analysis lacks end-to-end latency characterization

The runtime analysis (page 6) reports individual component times summing to 90.31 ± 6.84 ms total, achieving >10 Hz refresh rate. However, this only accounts for the US probe tracking pipeline. The total system latency including needle tracking, data transmission overhead, HMD rendering, and the fusion visualization is not reported. For a clinical navigation system, end-to-end latency from physical movement to visual update is the critical metric. The authors should provide a complete latency breakdown.

**Comment 8:** Comparison with marker-based tracker is limited in scope

The comparison with ClaroNav MicronTracker (Section: Comparison to Marker-based Tracker, page 5) only evaluates relative motion (translation and rotation changes), not absolute positioning accuracy. While relative motion comparison avoids coordinate system alignment issues, absolute accuracy in the world coordinate system is what ultimately matters for clinical navigation. The authors should discuss this limitation and, if possible, provide absolute accuracy measurements using a common reference frame.

**Comment 9:** Training data collection and annotation methodology needs clarification

The ablation study mentions that "Both models were trained on almost 16000 images and tested on 2200 images gathered using Intel Realsense D455 and D435i stereo cameras" (page 4). However, the actual clinical system uses HoloLens 2's built-in cameras. The domain gap between Intel RealSense training data and HoloLens 2 deployment data is not addressed. How does the model generalize across these different camera systems? Were any domain adaptation techniques employed? This is critical for validating the claimed accuracy in the actual deployment setting.

**Comment 10:** Figure 2 labeling inconsistency

Figure 2 (page 3) uses labels "(a)" and "(b)" in the caption text but uses "A" and "B" in the actual figure. This labeling should be consistent throughout the manuscript. The same inconsistency appears in Figure 5 (caption uses (a)-(d), figure uses A-D), Figure 6 (caption uses (a)-(b), figure uses A-B), and Figure 7 (caption uses (a)-(c), figure uses A-C).

**Comment 11:** Insufficient description of patient registration accuracy

The patient registration process (Section: Mixed reality visualization and patient registration, page 2) relies on manually matching corresponding points between imaging data and physical sites using radiological markers. The accuracy of this critical step is not independently evaluated. Since all downstream fusion accuracy depends on this initial registration, the authors should report the fiducial registration error (FRE) and target registration error (TRE) of this step separately from the overall CT-US fusion error.

**Comment 12:** Missing comparison with state-of-the-art registration methods

The discussion (page 9) mentions several competing approaches (Gueziri et al., Wei et al., Chi et al., Wang et al.) with their respective registration errors. However, the paper does not provide a structured, fair comparison table. The evaluation conditions differ significantly across studies (different anatomies, phantoms, imaging modalities). The authors should at minimum create a comparison table clearly noting the differences in experimental conditions, or ideally benchmark their approach against at least one competing method under identical conditions.

**Comment 13:** No user study or ergonomic evaluation

For a mixed reality system intended for clinical use, user experience and ergonomic factors are crucial. The paper does not report any user study evaluating factors such as: cognitive load during the procedure, comfort of wearing the HMD during extended procedures, visual fatigue, ease of the gesture/voice interface, or learning curve. Given that the introduction mentions the system uses "gestures and voice commands," a formal usability assessment would strengthen the clinical applicability claims.

**Comment 14:** Typo — "ZberaPose" instead of "ZebraPose"

On page 5, in the sentence "when using ZberaPose with Prog-X alone," the name is misspelled as "ZberaPose." It should be "ZebraPose" to maintain consistency with the rest of the manuscript.

**Comment 15:** Figure 4 — axis labels and legend text are too small

In Figure 4 (page 5), the axis labels ("Threshold [cm]", "Threshold [px]", "Recall") and the legend text are very small and difficult to read, especially in print format. The font size should be increased to ensure readability. Additionally, the legend placement overlaps with some data curves in certain subplots, reducing clarity.

**Comment 16:** The "single index finder tip" typo

On page 7, the sentence reads "The puncture site was selected with single index finder tip." This appears to be a typo — "finder" should likely be "finger."

**Comment 17:** Novelty over the authors' prior work (Ref. 24) is unclear

The present work builds upon the authors' previously published system (Ref. 24, Trojak et al., Cancers, 2024). While the introduction mentions that the current work "incorporates markerless US probe tracking," the specific novel contributions beyond Ref. 24 should be more clearly delineated. A dedicated paragraph or subsection explicitly listing the new contributions versus the prior work would help readers and reviewers assess the incremental novelty.

**Comment 18:** Lack of failure case analysis

The paper reports overall accuracy metrics but does not analyze failure cases. For example, in the biopsy navigation assessment, 12.86% of attempts with MR navigation still missed the target. What caused these failures? Were they related to tracking loss, registration error, or operator error? Similarly, in the pose estimation, what scenarios lead to the largest errors? A failure case analysis would provide valuable insights for future improvements.

**Comment 19:** References contain a mix of recent and dated sources without justification

While many references are recent (2021-2025), some foundational references are quite old (e.g., Ref. 36, Arun et al., 1987 for least-squares fitting). This is acceptable for well-established methods. However, for the deep learning and mixed reality components, some highly relevant recent works may be missing. For instance, recent advances in real-time 6DoF pose estimation beyond ZebraPose, PVNet, and HiPose (e.g., FoundationPose, GigaPose, or other 2024-2025 methods) are not discussed. The related work section should be updated to reflect the current state of the art more comprehensively.

**Comment 20:** The survival function analysis methodology is questionable

In the CT-US Target Fusion Error section (page 7-8), the authors fit a "4th degree polynomial" as a survival function to the error distribution and use the 0.95 intersection to claim errors remain within 3.41 mm. A polynomial is not a standard survival function model — Kaplan-Meier estimators or parametric models (Weibull, exponential) are the standard approaches in reliability/survival analysis. A 4th degree polynomial is not guaranteed to be monotonically decreasing or bounded between 0 and 1, making it a potentially unreliable estimator. The authors should justify this methodological choice or adopt standard survival analysis techniques.

---

*This review was generated by Paper Reviewer Pro.*
