from sentence_transformers import SentenceTransformer
from datasets import load_dataset
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt

class SentenceModel():
    def __init__(self, model_name):
        self.model = SentenceTransformer(model_name)

    def inference(self, input_text):
        embeddings = self.model.encode([input_text])
        return embeddings

def show(datasets, model_name):
    model = SentenceModel(model_name)

    titles = []
    vec_arr = []
    for d in datasets:
        titles.append(d['title'])
        arr = model.inference(d['text'])
        vec_arr.append(arr)

    tsne = TSNE(n_components=2, random_state=42)
    embeddings_2d = tsne.fit_transform(vec_arr)

    plt.figure(figsize=(10, 8))
    plt.scatter(embeddings_2d[:, 0], embeddings_2d[:, 1], c='blue', marker='o')
    plt.title(model_name)
    plt.xlabel('Dimension 1')
    plt.ylabel('Dimension 2')

    for i, text in enumerate(titles):
        plt.annotate(text[:15], (embeddings_2d[i, 0], embeddings_2d[i, 1]))

    plt.show()

def main():
    dataset = load_dataset('izumi-lab/wikipedia-ja-20230720', split='train')
    ds = dataset.shuffle(seed=42).select(range(100))

    models = [
        'intfloat/multilingual-e5-large',
        'pkshatech/GLuCoSE-base-ja',
        'cl-nagoya/sup-simcse-ja-base',
        'cl-nagoya/ruri-base'
    ]
    for m in models:
        show(ds, m)





if __name__ == '__main__':
    main()